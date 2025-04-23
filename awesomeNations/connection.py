from awesomeNations.customMethods import join_keys, string_is_number
from awesomeNations.exceptions import HTTPError, DataError
from awesomeNations.internalTools import _AwesomeParser
from awesomeNations.internalTools import _NationAuth
from typing import Optional, Literal, Any
from pprint import pprint as pp
from pathlib import Path
import urllib3
import logging
import time
import requests
from requests import Response

logger = logging.getLogger("AwesomeLogger")

parser = _AwesomeParser()

class _WrapperConnection():
    def __init__(self,

                 ):
        self._headers: dict = None
        self._request_timeout: int | tuple = None
        self._ratelimit_sleep: bool = None
        self._ratelimit_reset_time: int = None
        self._ratelimit_remaining: int = None
        self._api_version: int = None
        self._allow_beta: bool = False
        self.base_url = "https://www.nationstates.net/cgi-bin/api.cgi"
        
        #self._pool_manager = urllib3.PoolManager(4,
        #                                        self.headers,
        #                                        retries=False)
        self._auth: Optional[_NationAuth] = None

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
                       url: str = 'https://www.nationstates.net/') -> dict:
        """
        This fetches API data and automatically parses it: (xml response -> python dictionary)
        """
        time.sleep(0.5)
        url = url.format(v=self._api_version)
        logger.debug(f"Fetching API data: {url}")
        
        # Updates headers X-Password, X-Autologin and X-Pin in the next request
        # for actions that need authentication (Like private shards).
        self._update_auth()

        #response = self._pool_manager.request("GET", url, headers=self.headers, fields=query_parameters, timeout=self.request_timeout)
        response = requests.get(url, headers=self._headers, timeout=self._request_timeout)
        self.process_response(response)

        parsed_response = parser.parse_xml(response)
        return parsed_response

    def fetch_raw_data(self,
                       url: str) -> str:
        logger.debug(f"Fetching raw data: {url}")
        
        response = requests.get(url, headers=self._headers, timeout=self._request_timeout)
        self.process_response(response)
        
        return response.text

    def connection_status_code(self, url: str = 'https://www.nationstates.net/') -> int:
        url = url.format(v=self._api_version)
        
        response = requests.get(url, headers=self._headers, timeout=self._request_timeout)
        
        self.update_ratelimit_status(response.headers)
        
        logger.debug(f"{url}: {response.status_code}")

        return response.status_code
   
    def check_api_ratelimit(self) -> None:
        """
        Checks the NationStates API ratelimit and hibernates if the request limit was reached.
        """
        if self._ratelimit_sleep:
            if self._ratelimit_remaining != None and self._ratelimit_remaining < 1:
                    logger.warning(f"API ratelimit reached, your code will be paused for: {self._ratelimit_reset_time} seconds.")
                    time.sleep(self._ratelimit_reset_time + 1)
                    logger.info("Hibernation finished")

    def update_ratelimit_status(self, response_headers: dict) -> None:
        self._ratelimit_remaining = self.get_header(response_headers, "Ratelimit-remaining")
        self.check_api_ratelimit()

    def get_header(self, headers: dict, key: str, default = None) -> int | None:
        output_value: Any | None = default
        key_value: str | None = headers.get(key)
        if key_value:
            output_value = key_value
            if string_is_number(key_value):
                output_value = int(key_value)
        return output_value

    def _update_auth(self, response_headers: Optional[dict[str, Any]]= None) -> None:
        x_pin_header: int | None = self.get_header(response_headers, "X-Pin") if response_headers else None
        
        # Updates self._auth X-Pin if necessary (for quick sucessive requests):
        if self._auth:
            if x_pin_header:
                if self._auth.xpin != x_pin_header:
                    self._auth.xpin = x_pin_header
            self._headers.update(self._auth.get())

    def process_response(self, response: Response) -> None:
        if response.status_code != 200:
            raise HTTPError(response.status_code)
        
        self._update_auth(response.headers)

        self.update_ratelimit_status(response.headers)

if __name__ == "__main__":
    wrapper = _WrapperConnection()
    wrapper.set(aaa="test")