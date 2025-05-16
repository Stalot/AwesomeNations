from awesomeNations.customMethods import join_keys, string_is_number
from awesomeNations.exceptions import HTTPError, DataError, ConnectionError
from awesomeNations.internalTools import _AwesomeParser
from awesomeNations.internalTools import _NationAuth, _Secret
from typing import Optional, Literal, Any
from urllib3 import BaseHTTPResponse, HTTPResponse, HTTPHeaderDict
from pprint import pprint as pp
from pathlib import Path
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
        if content_encoding:
            try:
                self.encoding = content_encoding.split(" ")[1].replace("charset=", "")
            except:
                pass
    
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
    
    def get_header(self, name: str, default = None) -> Optional[Any]:
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
        self.auth: Optional[_NationAuth] = None

    def setup(self, **kwargs) -> None:
        """
        Configures _WrapperConnection attributes from the given kwargs.
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"_WrapperConnection has no attribute '{key}'. Did you mean one of these: {", ".join(self.__dict__.keys())}?")

    def fetch_api_data(self,
                       url: str = 'https://www.nationstates.net/',
                       query_parameters: Optional[dict] = None) -> dict[str, dict[str, str | int | float]]:
        """
        This fetches API data and automatically parses it: (xml response -> python dictionary)
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

    def connection_status_code(self, url: str = 'https://www.nationstates.net/') -> int:
        url = url.format(v=self.api_version)
        
        self._update_auth()

        response: _NSResponse = self._make_request(url=url, raise_exception=False)
        self._process_response(response)

        return response.status
   
    def _check_api_ratelimit(self) -> None:
        """
        Checks the NationStates API ratelimit and hibernates if the request limit was reached.
        """
        if self.ratelimit_sleep:
            if self.ratelimit_remaining != None and self.ratelimit_remaining < 1:
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
        x_pin_header: Optional[int] = response.get_header("X-Pin") if response else None
        
        # Updates self.auth X-Pin if necessary (for quick sucessive requests):
        if self.auth:
            if x_pin_header:
                if self.auth.xpin != x_pin_header:
                    self.auth.xpin = _Secret(str(x_pin_header))
            self.headers.update(self.auth.get())

    def _process_response(self, response: _NSResponse) -> None:     
        self._update_auth(response)
        self._update_ratelimit_status(response)

if __name__ == "__main__":
    ...