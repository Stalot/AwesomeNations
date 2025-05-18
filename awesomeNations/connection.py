from awesomeNations.customMethods import format_key, gen_params
from awesomeNations.exceptions import HTTPError, ConnectionError
from awesomeNations.internalTools import _AwesomeParser, _ShardsQuery
from awesomeNations.internalTools import _Secret, _AuthManager
from awesomeNations.internalTools import _PrivateCommand
from typing import Optional, Literal, Any, Iterable
from urllib3 import BaseHTTPResponse, HTTPHeaderDict
import urllib3
import logging
import time

logger = logging.getLogger("AwesomeLogger")


class _NSResponse():
    def __init__(self, response: BaseHTTPResponse):
        self._response: BaseHTTPResponse = response
        self.content: bytes = self._response.data
        self.status: int = self._response.status
        self.headers: HTTPHeaderDict = self._response.headers
        self.encoding = "UTF-8"
        self._parser = _AwesomeParser()

        content_encoding: Optional[str] = self.headers.get("Content-Type")

        try:
            if content_encoding:
                self.encoding = content_encoding.split(" ")[1]
                self.encoding = self.encoding.replace("charset=", "")
        except Exception:
            self.encoding = "UTF-8"

    def __repr__(self):
        return f"_NSResponse(response: HTTPResponse = {self._response})"

    def get_content(self) -> dict[str, Any]:
        """
        Gets response content and automatically parses it.
        """
        parsed_data: dict = self._parser.parse_xml(self.content, self.encoding)
        return parsed_data

    def get_raw_content(self) -> str:
        """
        Gets response content without parsing it.
        """
        return self.content.decode(self.encoding).strip()

    def get_header(self,
                   name: str,
                   default=None) -> Optional[Any]:
        return self.headers.get(name, default)


class _WrapperConnection():
    def __init__(self):
        self.headers: dict[str, str] = {}
        self.request_timeout: int | tuple = (10, 10)
        self.ratelimit_sleep: bool = True
        self.ratelimit_reset_time: int = 30
        self.ratelimit_remaining: int = 50
        self.ratelimit_requests_seen: int = 0
        self.api_version: int = 12
        self.allow_beta: bool = False
        self.base_url = "https://www.nationstates.net/cgi-bin/api.cgi"

        self._pool_manager = urllib3.PoolManager(8,
                                                 self.headers,
                                                 retries=False)
        self.authManager = _AuthManager()
        self.auth_target: Optional[str] = None

    def setup(self, **kwargs) -> None:
        """
        Configures _WrapperConnection attributes from the given kwargs.
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                attrs: str = ", ".join(self.__dict__.keys())
                msg: str = f"{type(self).__name__} has no attribute '{key}'"
                raise AttributeError(f"{msg}. Did you mean {attrs}?")

    def fetch_api_data(self,
                       url: str = 'https://www.nationstates.net/') -> dict[str, dict[str, str | int | float]]:
        """
        This fetches API data and automatically
        parses it: (xml response -> python dictionary)
        """
        url = url.format(v=self.api_version)

        # Updates headers X-Password, X-Autologin and X-Pin in the next request
        # for actions that need authentication (Like private shards).
        self._update_auth()

        response: _NSResponse = self._make_request(url=url)
        self._process_response(response)

        return response.get_content()

    def fetch_raw_data(self,
                       url: str) -> str:

        response: _NSResponse = self._make_request(url=url)
        self._process_response(response)

        return response.get_raw_content()

    def connection_status_code(self,
                               url: str = 'https://www.nationstates.net/') -> int:
        url = url.format(v=self.api_version)

        self._update_auth()

        response: _NSResponse = self._make_request(url=url,
                                                   raise_exception=False)
        self._process_response(response)

        return response.status

    def _check_api_ratelimit(self) -> None:
        """
        Checks the NationStates API ratelimit and
        hibernates if the request limit was reached.
        """
        if self.ratelimit_sleep and self.ratelimit_remaining is not None:
            if self.ratelimit_remaining < 1:
                logger.warning(f"API ratelimit reached, your code will be paused for: {self.ratelimit_reset_time} seconds.")
                time.sleep(self.ratelimit_reset_time + 1)
                logger.info("Ratelimit hibernation finished.")

    def _update_ratelimit_status(self, response: _NSResponse) -> None:
        self.ratelimit_remaining = int(str(response.get_header("Ratelimit-remaining", 50)))
        self.ratelimit_requests_seen = int(str(response.get_header("X-ratelimit-requests-seen", 0)))
        self._check_api_ratelimit()

    def _make_request(self, method: str = "GET", url: str = "www.example.com", raise_exception: bool = True) -> _NSResponse:
        match method:
            case "GET":
                logger.debug(f"GET: {url}")
            case "POST":
                logger.debug(f"POST: {url}")
            case _:
                raise ValueError(f"Method '{method}' is invalid.")
        try:
            ns_response = _NSResponse(self._pool_manager.request(method, url, headers=self.headers, timeout=self.request_timeout))
            logger.debug(f"{ns_response.status}")
            if ns_response.status != 200 and raise_exception:
                raise HTTPError(ns_response.status)
            return ns_response
        except urllib3.exceptions.NameResolutionError as e:
            raise ConnectionError(str(e))

    def _update_auth(self, response: Optional[_NSResponse] = None) -> None:
        x_pin_header: Optional[_Secret] = _Secret(response.get_header("X-Pin")) if response else None
        
        if self.auth_target:
            self.authManager.update_auth(self.auth_target, xpin=x_pin_header)
            self.headers.update(self.authManager.get(self.auth_target).get())

    def _process_response(self, response: _NSResponse) -> None:     
        self._update_auth(response)
        self._update_ratelimit_status(response)


class _APIBlock():
    def __init__(self) -> None:
        self.name: Optional[str] = None
        self._wrapper: _WrapperConnection
        self._parser: _AwesomeParser
        
        if self.name and not isinstance(self.name, str):
            raise ValueError(f"name must be type str, not '{type(self.name).__name__}'.")
    
    def _request_shards(self, shards: Optional[Iterable[str]], parammeters: Optional[dict[str, Any]]) -> dict[str, dict[str, Any]]:
        if self._wrapper:
            self._set_auth_target(self.name)
            url = self._wrapper.base_url + _ShardsQuery(("nation", self.name), shards, parammeters).querystring()
            response: dict[str, dict[str, Any]] = self._wrapper.fetch_api_data(url)
            return response
        raise ValueError("_wrapper must be set first.")
    
    def _set_wrapper(self, instance: _WrapperConnection):
        self._wrapper = instance
    
    def _set_auth_target(self, target: Optional[str]) -> None:
        setattr(self._wrapper, 'auth_target', target)


class _NationAPI(_APIBlock):
    """
    Class dedicated to NationStates nation API.
    """
    def __init__(self,
                    nation_name: str) -> None:
        super().__init__()
        self.name = format_key(nation_name, False, '%20') # Name is automatically parsed.
        self.password: Optional[_Secret] = None
        self.autologin: Optional[_Secret] = None

    def __repr__(self):
        return f"Nation(nation_name='{self.name}', password={self.password}, autologin={self.autologin})"

    def __enter__(self, *args, **kwargs):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self._wrapper.authManager.forget(self.name)
        del self

    def set_auth(self, password: Optional[str] = None, autologin: Optional[str] = None) -> None:
        """
        Sets Nation authentication.
        """
        if password:
            self.password = _Secret(password)
        if autologin:
            self.autologin = _Secret(autologin)
        if not password and not autologin:
            raise ValueError("At least a password or an autologin must be given.")
        self._wrapper.authManager.update_auth(self.name, self.password, self.autologin)

    def exists(self) -> bool:
        """
        Checks if nation exists.
        """
        url = self._wrapper.base_url + _ShardsQuery(("nation", self.name)).querystring()
        status_code: int = self._wrapper.connection_status_code(url)
        match status_code:
            case 200:
                return True
            case 404:
                return False
            case _:
                raise HTTPError(status_code)

    # DEPRECATED METHOD
    def get_public_shards(self,
                            shards: Optional[str | tuple[str, ...] | list[str]] = None,
                            **kwargs) -> dict[str, dict[str, Any]]:
        """
        # THIS METHOD IS DEPRECATED
        ## Use ```get_shards()``` instead!
        
        ***
        
        Gets one or more shards from the requested nation, returns the standard API if no shards provided.
        
        ### Standard:
        
        > A compendium of the most commonly sought information.
        
        ### Shards:
        > If you don't need most of this data, please use shards instead. Shards allow you to request
        > exactly what you want and can be used to request data not available from the Standard API!
        """
        url = self._wrapper.base_url + _ShardsQuery(("nation", self.name), shards, kwargs).querystring()
        logger.warning("get_public_shards() is deprecated, use get_shards() instead.")
        response: dict = self._wrapper.fetch_api_data(url)
        return response

    # Replacing get_public_shards()
    def get_shards(self,
                    shards: Optional[str | tuple[str, ...] | list[str]] = None,
                    **kwargs) -> dict[str, dict[str, Any]]:
        """
        Gets one or more shards from the requested nation, returns the standard API if no shards provided.
        
        ### Standard:
        
        > A compendium of the most commonly sought information.
        
        ### Shards:
        > If you don't need most of this data, please use shards instead. Shards allow you to request
        > exactly what you want and can be used to request data not available from the Standard API!
        """
        return self._request_shards(shards, kwargs)

    def is_authenticated(self) -> bool:
        """
        Checks if nation has a valid authentication.
        """
        try:
            self._wrapper.authManager.get(self.name)
            self.get_shards("ping")
            return True
        except (KeyError, HTTPError):
            return False

    def dispatch(self,
                 action: Literal["add", "edit", "remove"],
                 id: Optional[int] = None,
                 title: Optional[str] = None,
                 text: Optional[str] = None,
                 category: Optional[int] = None,
                 subcategory: Optional[int] = None
                 ) -> dict[str, dict[str, Any]]:
        """
        # BETA:
        Currently in development. Subject to change without warning.
        
        ---
        
        Creates, edits and deletes dispatches.
        
        When adding or editing a dispatch, specify: `title`, `text`, `category` and `subcategory`.
        When editing or removing a dispatch, you must also specify `id`.
        """
        if action != "add" and action != "edit" and action != "remove":
            raise ValueError(f"action must be 'add', 'edit' or 'remove', not '{action}'.")
        if not action == "add" and not id:
            raise ValueError(f"action '{action}' needs a valid dispatch id!")
        if (action == "add" or action == "edit") and not all((title, text, category, subcategory)):
            raise ValueError(f"action '{action}' needs a valid title, text, category and subcategory.")

        if id and not isinstance(id, int):
            raise ValueError(f"id must be int, not type '{type(id).__name__}'.")
        if title and not isinstance(title, str):
            raise ValueError(f"title must be str, not type '{type(title).__name__}'.")
        if text and not isinstance(text, str):
            raise ValueError(f"text must be str, not type '{type(text).__name__}'.")
        if category and not isinstance(category, int):
            raise ValueError(f"category must be int, not type '{type(category).__name__}'.")
        if subcategory and not isinstance(subcategory, int):
            raise ValueError(f"subcategory must be int, not type '{type(subcategory).__name__}'.")
        
        query_params_raw: dict[str, Optional[str | list[str]]] = {
            "dispatchid": str(id) if id is not None else None,
            "dispatch": str(action) if action else None,
            "title": title.replace(" ", "%20") if title else None,
            "text": text.replace(" ", "%20") if text else None,
            "category": str(category) if category is not None else None,
            "subcategory": str(subcategory) if subcategory is not None else None
        }
        # Remove keys with None values
        query_params: dict[str, str | list[str]] = {k: v for k, v in query_params_raw.items() if v is not None}
        
        return self._execute_command('dispatch', query_params)

    def rmb_post(self,
                    region: str,
                    text: str) -> dict[str, dict[str, Any]]:
        """
        # BETA:
        Currently in development. Subject to change without warning.
        
        ---
        
        Post to a regional RMB.
        """
        if not isinstance(region, str):
            raise ValueError(f"region must be type str, not {type(region).__name__}.")
        if not isinstance(text, str):
            raise ValueError(f"text must be type str, not {type(text).__name__}.")

        query_params: dict[str, Any] = {
            'nation': self.name,
            'region': format_key(region, replace_empty="%20"),
            'text': text.replace(" ", "%20") if text else text
        }
        
        return self._execute_command('rmbpost', query_params)

    def gift_card(self,
                    id: int,
                    season: int,
                    to: str) -> dict[str, dict[str, Any]]:
        """
        # BETA:
        Currently in development. Subject to change without warning.
        
        ---
        
        Gift a Trading Card to someone else.
        """
        if not isinstance(id, int):
            raise ValueError(f"id must be type int, not {type(id).__name__}.")
        if not isinstance(season, int):
            raise ValueError(f"season must be type int, not {type(season).__name__}.")
        if not isinstance(to, str):
            raise ValueError(f"to must be type str, not {type(to).__name__}.")

        query_params: dict[str, Any] = {
            "cardid": id,
            "season": season,
            "to": format_key(to, replace_empty="_"),
        }
        return self._execute_command('giftcard', query_params)

    def answer_issue(self,
                    id: int,
                    option: int) -> dict[str, dict[str, Any]]:
        """
        Address an Issue.

        To dismiss an issue, set `option` to -1 (Note that option id numbers
        begin counting at zero).
        """     
        if not isinstance(id, int):
            raise ValueError(f"id must be type int, not {type(id).__name__}.")
        if not isinstance(option, int):
            raise ValueError(f"option must be type int, not {type(option).__name__}.")
                            
        query_params: dict[str, Any] = {
            "issue": str(id),
            "option": str(option),
        }
        return self._execute_command('issue', query_params)

    def _execute_command(self,
                        c: Literal["issue", "giftcard", "dispatch", "rmbpost"],
                        parameters: dict[str, Any]) -> dict[str, dict[str, Any]]:
        """
        Executes private commands.
        """
        if not isinstance(c, str):
            raise ValueError(f"c must be type str, not {type(c).__name__}.")
        
        self._set_auth_target(self.name)
        
        command = _PrivateCommand(self.name,
                                    c,
                                    parameters,
                                    self._wrapper.allow_beta)
        token: Optional[str] = None
        if not c in command.not_prepare:
            logger.info(f"Preparing private command: '{c}'...") 
            prepare_response: dict = self._wrapper.fetch_api_data(self._wrapper.base_url + command.command("prepare"))
            token: Optional[str] = prepare_response["nation"].get("success")
            if not token:
                return prepare_response

        logger.info(f"Executing private command: '{c}'...")
        execute_response: dict = self._wrapper.fetch_api_data(self._wrapper.base_url + command.command("execute", token))
        return execute_response

class _RegionAPI(_APIBlock): 
    """
    Class dedicated to NationStates region API.
    """
    def __init__(self, region_name: str) -> None:
        self.name = format_key(region_name, False, '%20')
    
    def __repr__(self):
        return f"{type(self).__name__}(region_name='{self.name}')"
    
    def __enter__(self, *args, **kwargs):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        del self
    
    def exists(self) -> bool:
        """
        Checks if region exists.
        """
        url = wrapper.base_url + _ShardsQuery(("region", self.name)).querystring()
        status_code: int = wrapper.connection_status_code(url)
        match status_code:
            case 200:
                return True
            case 404:
                return False
            case _:
                raise HTTPError(status_code)

    def get_shards(self, shards: Optional[str | tuple[str, ...] | list[str]] = None, **kwargs) -> dict[str, dict[str, Any]]:
        """
        Gets one or more shards from the requested region, returns the
        standard API if no shards provided.
        
        ### Standard:
        
        > A compendium of the most commonly sought information.
        
        ### Shards:
        > If you don't need most of this data, please use
        > shards instead. Shards allow you to request
        > exactly what you want and can be used to request 
        : data not available from the Standard API!
        """
        return self._request_shards(shards, kwargs)


if __name__ == "__main__":
    wrapper = _WrapperConnection()
