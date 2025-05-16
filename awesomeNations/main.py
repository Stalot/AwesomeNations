from awesomeNations.connection import _WrapperConnection
from awesomeNations.customMethods import format_key, gen_params, generate_epoch_timestamp
from awesomeNations.internalTools import _NationAuth, _ShardsQuery, _DailyDataDumps, _PrivateCommand, _Secret, _AwesomeParser
from awesomeNations.exceptions import HTTPError
from pprint import pprint as pp
from datetime import datetime
from typing import Optional
from urllib3 import Timeout
from typing import Literal, Any, AnyStr
from pathlib import Path
from logging import WARNING, DEBUG
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger("AwesomeLogger")
logging.basicConfig(level=logging.WARNING, format="[%(asctime)s] %(levelname)s: %(message)s")

wrapper = _WrapperConnection()
parser = _AwesomeParser()

class AwesomeNations():
    """
    # 🚩 AwesomeNations 🚩

    Welcome! I'm the main class of this library and can't wait to collaborate with you!
    Feel free to explore my [GitHub repository](https://github.com/Stalot/AwesomeNations)
    and report any issues [here](https://github.com/Stalot/AwesomeNations/issues).

    # 📚 Useful References 📚
    
    If you want to make things right, I highly recommend you to **read documentation**.
    Yes, I know, it sounds as thrilling as watching paint dry... But you really should!
    Here are some helpful links for coding guidelines and references. Please note that
    these resources may change over time:

    - 📖 [NationStates API Documentation](https://www.nationstates.net/pages/api.html)  
    - ⚖️ [NationStates Script Rules for HTML site](https://forum.nationstates.net/viewtopic.php?p=16394966#p16394966)
    
    ---
    
    ### user_agent:

    > Sets a User-Agent. Whenever possible, your tool should identify itself by setting
    > the User-Agent header with **relevant** data.

    > - `<application name>/<version> <comments>`
    > - `ExampleScript/1.2 (by:Testlandia; usedBy:Maxtopia)`
    
    ### request_timeout:

    > Defines a timeout (in seconds) for requests.

    > - `request_timeout: tuple = (10, 5)` -> 10 seconds for connecting, 5 seconds for reading.
    > - `request_timeout: int = 10` -> 10 seconds for both.
    
    ### ratelimit_sleep:
    
    > This allows to automatically "sleep" if the API ratelimit is reached, prevents temporary
    > lockouts due to excessive requests in a short span of time.

    ### ratelimit_reset_time:
    
    > Defines the reset time (in seconds) to wait when the API ratelimit is reached.
    
    ### api_version:
    
    > This setting allows you to specify the NationStates API version your script uses.

    ### log_level:
    
    > Sets logging log level, if None is given, disables logging.

    ### allow_beta:
    
    > Defines if AwesomeNations should allow beta resources to be used by you or not.
    """

    def __init__(self,
                 user_agent: str,
                 request_timeout: int | tuple = (15, 10),
                 ratelimit_sleep: bool = True,
                 ratelimit_reset_time: int = 30,
                 api_version: int = 12,
                 log_level: Optional[int] = WARNING,
                 allow_beta: bool = False):
        self.user_agent = user_agent
        self.request_timeout: int | tuple[int, int] = request_timeout
        self.ratelimit_sleep: bool = ratelimit_sleep
        self.ratelimit_reset_time: int = ratelimit_reset_time
        self.api_version: int = api_version
        self.log_level: Optional[int] = log_level
        self.allow_beta = allow_beta

        self._wrapper_headers: dict[str, str] = {
        "User-Agent": "",
        "Cache-Control": "no-cache",
        }
        
        self.set_user_agent(self.user_agent)
        
        if self.log_level is None:
            logger.disabled = True
        elif type(self.log_level) is int:
            logger.level = self.log_level
        else:
            raise ValueError(f"Invalid {type(self.log_level).__name__} '{self.log_level}', log_level must be an int (to change level) or None (to disable logging)")
        
        if isinstance(self.request_timeout, tuple):
            self.request_timeout = Timeout(connect=(self.request_timeout[0]), read=self.request_timeout[1]) # type: ignore
        wrapper.setup(
            request_timeout = self.request_timeout,
            ratelimit_sleep = self.ratelimit_sleep,
            ratelimit_reset_time = self.ratelimit_reset_time,
            api_version = self.api_version,
            allow_beta = self.allow_beta
        )

    def __repr__(self):
        return f"AwesomeNations(user_agent='{self.user_agent}', request_timeout={self.request_timeout}, ratelimit_sleep={self.ratelimit_sleep}, ratelimit_reset_time={self.ratelimit_reset_time}, api_version={self.api_version}, log_level={self.log_level}, allow_beta={self.allow_beta})"

    def today_is_nationstates_birthday(self) -> bool:
        "Today is 11/13?"
        today = datetime.today()
        date: str = today.strftime('%D')
        birthday: bool = False
        if '11/13' in date:
            birthday = True
        return birthday

    def get_nationstates_age(self) -> int:
        "Current year - NationStates year of creation (NationStates was created in 2002)."
        created = 2002
        today = datetime.today().year
        age = today - created
        return age

    def get_daily_data_dumps(self,
                             filepath: str | Path = "./datadump.gz",
                             type: Literal["nation", "region"] = "nation") -> None:
        """
        Dowloads NationStates daily data dumps.
        
        ### type: str
        
        - "nation": Dowloads the nation data dump.
        - "region": Dowloads the region data dump.
        """
        dumps = _DailyDataDumps()
        return dumps.dowload(dumps.get_dump(type), filepath)

    def get_world_shards(self,
                         shards: str | tuple[str, ...] | list[str],
                         **kwargs: Any) -> dict[str, dict[str, Any]]:
        """
        Gets one or more shards from the World API.
        """
        if not shards:
            raise ValueError("No shards provided and World API doesn't have a standard API.")
        url = wrapper.base_url + _ShardsQuery(("world", None), shards, kwargs).querystring() # type: ignore
        response: dict = wrapper.fetch_api_data(url)
        return response

    def get_world_assembly_shards(self,
                                  shards: str | tuple[str, ...] | list[str],
                                  **kwargs: Any) -> dict[str, dict[str, Any]]:
        """
        Gets one or more shards from the World Assembly API.
        """
        if not shards:
            raise ValueError("No shards provided and World Assembly API doesn't have a standard API.")
        council_id = kwargs["council_id"]
        kwargs.pop("council_id")
        url = wrapper.base_url + _ShardsQuery(("wa", council_id), shards, kwargs).querystring()
        response: dict = wrapper.fetch_api_data(url)
        return response

    def get_api_latest_version(self) -> int:
        """Gets NationStates API latest version"""
        url = "https://www.nationstates.net/cgi-bin/api.cgi?a=version"
        latest_version: int = int(wrapper.fetch_raw_data(url))
        return latest_version

    def get_wrapper_status(self) -> dict[str, Any]:
        """
        Gets wrapper data, such the number of requests seen.
        """
        status: dict[str, Any] = {
            "status": {
                "ratelimit_requests_seen": getattr(wrapper, "ratelimit_requests_seen"),
            }
        }
        return status

    def set_user_agent(self, user_agent: str) -> None:
        """
        Sets AwesomeNations `user_agent`.
        """
        if not isinstance(user_agent, str):
            raise ValueError(f"user_agent must be type string, not {type(user_agent).__name__}")
        user_agent = user_agent.strip()
        if len(user_agent.replace(" ", "")) < 7:
            raise ValueError(f"'{user_agent}' is too short for a user_agent.")
        #setattr(self, "user_agent", user_agent)
        self._wrapper_headers.update({"User-Agent": user_agent})
        wrapper.headers.update(self._wrapper_headers)

    class Nation:
        """
        Class dedicated to NationStates nation API.
        """
        def __init__(self,
                     nation_name: str,
                     password: Optional[str] = None,
                     autologin: Optional[str] = None) -> None:
            self.nation_name: str = format_key(nation_name, False, '%20') # Name is automatically parsed.
            self.password: Optional[_Secret] = None
            self.autologin: Optional[_Secret] = None

            if password:
                if not isinstance(password, str):
                    raise ValueError(f"password must be type str, not {type(password).__name__}.")
                self.password = _Secret(password)
            if autologin:
                if not isinstance(autologin, str):
                    raise ValueError(f"autologin must be type str, not {type(autologin).__name__}.")
                self.autologin = _Secret(autologin)

            auth_password: Optional[str] = self.password.reveal() if self.password and isinstance(self.password, _Secret) else None
            auth_autologin: Optional[str] = self.autologin.reveal() if self.autologin and isinstance(self.autologin, _Secret) else None
            if any((auth_password, auth_autologin)):
                self.set_auth(auth_password, auth_autologin)

        def __repr__(self):
            return f"Nation(nation_name='{self.nation_name}', password={self.password}, autologin={self.autologin})"
    
        def __enter__(self, *args, **kwargs):
            return self
        
        def __exit__(self, exc_type, exc_value, traceback):
            #setattr(wrapper, "auth", None)
            wrapper.authManager.forget(self.nation_name)
            del self
    
        def __getattribute__(self, name):
            setattr(wrapper, "auth_target", object.__getattribute__(self, "nation_name"))
            return object.__getattribute__(self, name)
    
        def set_auth(self, password: Optional[str] = None, autologin: Optional[str] = None) -> None:
            """
            Sets Nation authentication.
            """
            if password:
                self.password = _Secret(password)
            if autologin:
                self.autologin = _Secret(autologin)
                #new_auth = _NationAuth(self.password, self.autologin)
                #setattr(wrapper, 'auth', new_auth)
            if not password and not autologin:
                raise ValueError("At least a password or an autologin must be given.")
            wrapper.authManager.update_auth(self.nation_name, self.password, self.autologin)
    
        def exists(self) -> bool:
            """
            Checks if nation exists.
            """
            url = wrapper.base_url + _ShardsQuery(("nation", self.nation_name)).querystring()
            status_code: int = wrapper.connection_status_code(url)
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
            url = wrapper.base_url + _ShardsQuery(("nation", self.nation_name), shards, kwargs).querystring()
            logger.warning("get_public_shards() is deprecated, use get_shards() instead.")
            response: dict = wrapper.fetch_api_data(url)
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
            url = wrapper.base_url + _ShardsQuery(("nation", self.nation_name), shards, kwargs).querystring()
            response: dict = wrapper.fetch_api_data(url)
            return response

        def is_authenticated(self) -> bool:
            """
            Checks if nation has a valid authentication.
            """
            try:
                wrapper.authManager.get(self.nation_name)
                self.get_shards("ping")
                return True
            except (KeyError, HTTPError):
                return False

        def execute_command(self,
                            c: Literal["issue", "giftcard", "dispatch", "rmbpost"],
                            **kwargs) -> dict[str, dict[str, Any]]:
            """
            Executes private commands.
            """
            if not isinstance(c, str):
                raise ValueError(f"c must be type str, not {type(c).__name__}.")
            command = _PrivateCommand(self.nation_name,
                                      c,
                                      kwargs,
                                      wrapper.allow_beta)
            token: str | None = None
            if not c in command.not_prepare:
                logger.info(f"Preparing private command: '{c}'...") 
                prepare_response: dict = wrapper.fetch_api_data(wrapper.base_url + command.command("prepare"))
                token: Optional[str] = prepare_response["nation"].get("success")
                if not token:
                    return prepare_response
    
            logger.info(f"Executing private command: '{c}'...")
            execute_response: dict = wrapper.fetch_api_data(wrapper.base_url + command.command("execute", token))
            return execute_response

        def dispatch(self,
                     action: Literal["add", "edit", "remove"],
                     id: Optional[int] = None,
                     title: Optional[str] = None,
                     text: Optional[str] = None,
                     category: Optional[int] = None,
                     subcategory: Optional[int] = None) -> dict[str, dict[str, Any]]:
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
            
            c = _PrivateCommand(self.nation_name, "dispatch", query_params, wrapper.allow_beta)

            prepare_response: dict = wrapper.fetch_api_data(wrapper.base_url + c.command("prepare"))
            token = prepare_response["nation"].get("success")
            
            if not token:
                reason = parser.parse_html_in_string(prepare_response["nation"]["error"])
                raise ValueError(reason)
            
            execute_response: dict = wrapper.fetch_api_data(wrapper.base_url + c.command("execute", token))
            
            error: Optional[str] = execute_response["nation"].get("error")
            if error:
                reason = parser.parse_html_in_string(error)
                raise ValueError(reason)
            
            return execute_response

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

            query_params: dict[str, str] = gen_params(join=True,
                                                      nation=self.nation_name,
                                                      region=format_key(region, replace_empty="%20"),
                                                      text=text.replace(" ", "%20") if text else text)
            
            c = _PrivateCommand(self.nation_name, "rmbpost", query_params, wrapper.allow_beta)

            prepare_response: dict[str, dict[str, Any]] = wrapper.fetch_api_data(wrapper.base_url + c.command("prepare"))
            token = prepare_response["nation"].get("success")
            
            if not token:
                raise ValueError(parser.parse_html_in_string(prepare_response["nation"]["error"]))
            
            execute_response: dict = wrapper.fetch_api_data(wrapper.base_url + c.command("execute", token))
            
            error: Optional[str] = execute_response["nation"].get("error")
            if error:
                raise ValueError(parser.parse_html_in_string(error))
            
            return execute_response

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
            query_params = {
                "cardid": id,
                "season": season,
                "to": format_key(to, replace_empty="_"),
            }
            
            c = _PrivateCommand(self.nation_name, "giftcard", query_params, wrapper.allow_beta)

            prepare_response: dict[str, dict[str, Any]] = wrapper.fetch_api_data(wrapper.base_url + c.command("prepare"))
            token = prepare_response["nation"].get("success")
            
            if not token:
                reason = parser.parse_html_in_string(prepare_response["nation"]["error"])
                raise ValueError(reason)
            
            execute_response: dict = wrapper.fetch_api_data(wrapper.base_url + c.command("execute", token))
            
            error: Optional[str] = execute_response["nation"].get("error")
            if error:
                reason = parser.parse_html_in_string(error)
                raise ValueError(reason)
            
            return execute_response

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
                               
            query_params: dict[str, str | list[str]] = {
                "issue": str(id),
                "option": str(option),
            }
            
            c = _PrivateCommand(self.nation_name, "issue", query_params, wrapper.allow_beta)
            
            execute_response: dict = wrapper.fetch_api_data(wrapper.base_url + c.command("execute"))
            
            error: Optional[str] = execute_response["nation"].get("issue").get("error")
            if error:
                reason = parser.parse_html_in_string(error)
                raise ValueError(reason)
            
            return execute_response

    class Region: 
        """
        Class dedicated to NationStates region API.
        """
        def __init__(self, region_name: str) -> None:
            self.region_name = format_key(region_name, False, '%20')
        
        def __repr__(self):
            return f"Region(region_name='{self.region_name}')"
        
        def __enter__(self, *args, **kwargs):
            return self
        
        def __exit__(self, exc_type, exc_value, traceback):
            del self
        
        def exists(self) -> bool:
            """
            Checks if region exists.
            """
            url = wrapper.base_url + _ShardsQuery(("region", self.region_name)).querystring()
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
            Gets one or more shards from the requested region, returns the standard API if no shards provided.
            
            ### Standard:
            
            > A compendium of the most commonly sought information.
            
            ### Shards:
            > If you don't need most of this data, please use shards instead. Shards allow you to request
            > exactly what you want and can be used to request data not available from the Standard API!
            """
            url = wrapper.base_url + _ShardsQuery(("region", self.region_name), shards, kwargs).querystring()
            response: dict = wrapper.fetch_api_data(url)
            return response

if __name__ == "__main__":
    api = AwesomeNations("AwesomeNations/Test", log_level=DEBUG)
    nation = api.Nation("Orlys")
    region = api.Region("Fullworthia")
    print(api)
    print(nation)
    print(region)