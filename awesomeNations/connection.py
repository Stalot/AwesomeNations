from awesomeNations.customMethods import join_keys, string_is_number
from awesomeNations.exceptions import HTTPError, DataError
from awesomeNations.internalTools import _AwesomeParser
from awesomeNations.internalTools import _NationAuth
from typing import Optional, Literal, Any
from urllib3 import BaseHTTPResponse
from pprint import pprint as pp
from pathlib import Path
import urllib3
import logging
import time

logger = logging.getLogger("AwesomeLogger")

parser = _AwesomeParser()

class _WrapperConnection():
    def __init__(self,
                 headers: dict = None,
                 ratelimit_sleep: bool = True,
                 ratelimit_reset_time: int = 30,
                 api_version: int = 12,
                 ):
        self.headers: dict = headers
        self.request_timeout: int | tuple = 10
        self.ratelimit_sleep: bool = ratelimit_sleep
        self.ratelimit_reset_time: int = ratelimit_reset_time
        self.ratelimit_remaining: int = None
        self.ratelimit_requests_seen: int = None
        self.api_version: int = api_version
        self.base_url = "https://www.nationstates.net/cgi-bin/api.cgi"
        
        self._pool_manager = urllib3.PoolManager(4,
                                                self.headers,
                                                retries=False)
        self.last_request_headers: dict = {}
        self._auth: Optional[_NationAuth] = None

    def fetch_api_data(self,
                       url: str = 'https://www.nationstates.net/',
                       query_parameters: Optional[dict] = None) -> dict:
        """
        This fetches API data and automatically parses it: (xml response -> python dictionary)
        """
        url = url.format(v=self.api_version)
        logger.debug(f"Fetching API data: {url}")
        
        # Updates headers X-Password, X-Autologin and X-Pin in the next request
        # for actions that need authentication (Like private shards).
        if self._auth:
            self.headers.update(self._auth.get())

        response = self._pool_manager.request("GET", url, headers=self.headers, fields=query_parameters, timeout=self.request_timeout)

        if response.status != 200:
            raise HTTPError(response.status)
        
        self.last_request_headers.update(response.headers)
        x_pin_header: int | None = response.headers.get("X-Pin")
        
        # Updates self._auth X-Pin if necessary (for quick sucessive requests):
        if self._auth and x_pin_header:
            if self._auth.xpin != x_pin_header:
                self._auth.xpin = x_pin_header

        self.update_ratelimit_status(response.headers)

        parsed_response = parser.parse_xml(self.decode_response_data(response))
        return parsed_response

    def fetch_raw_data(self,
                       url: str) -> str:
        logger.debug(f"Fetching raw data: {url}")
        
        response = self._pool_manager.request("GET", url)
        
        if response.status != 200:
            raise HTTPError(response.status)
        
        self.update_ratelimit_status(response.headers)
        
        return self.decode_response_data(response)["data"].strip()

    def connection_status_code(self, url: str = 'https://www.nationstates.net/') -> int:
        url = url.format(v=self.api_version)
        
        logger.debug(f"Testing connection status code of: {url}")
        
        response = self._pool_manager.request("GET", url, headers=self.headers, timeout=20)
        
        self.last_request_headers.update(response.headers)
        self.update_ratelimit_status(response.headers)
        
        logger.debug(f"{url} status code is: {response.status}")

        return response.status
   
    def check_api_ratelimit(self) -> None:
        """
        Checks the NationStates API ratelimit and hibernates if the request limit was reached.
        """
        if self.ratelimit_sleep:
            if self.ratelimit_remaining != None and self.ratelimit_remaining < 1:
                    logger.warning(f"API ratelimit reached, your code will be paused for: {self.ratelimit_reset_time} seconds.")
                    time.sleep(self.ratelimit_reset_time + 1)
                    logger.info("Hibernation finished")

    def update_ratelimit_status(self, response_headers: dict) -> None:
        self.ratelimit_remaining = self.get_header(response_headers, "Ratelimit-remaining")
        self.ratelimit_requests_seen = self.get_header(response_headers, "X-ratelimit-requests-seen")
        
        logger.info(f"Ratelimit remaining: {self.ratelimit_remaining}")
        
        self.check_api_ratelimit()

    def decode_response_data(self, response: BaseHTTPResponse) -> dict[str] | None:
        encodings: tuple[str] = ("UTF-8", "LATIN-1")
        tries: int = 0
        for enc in encodings:
            try:
                data = {
                    "encoding": enc,
                    "data": response.data.decode(enc)
                }
                return data
            except Exception as decoding_error:
                logger.warning(F"Failed to decode response using {enc}")
                tries += 1
                if tries >= len(encodings):
                    raise DataError("API Response", "Decoding error.")

    def get_header(self, headers: dict, key: str, default = None) -> int | None:
        output_value: Any | None = default
        key_value: str | None = headers.get(key)
        if key_value:
            output_value = key_value
            if string_is_number(key_value):
                output_value = int(key_value)
        return output_value

if __name__ == "__main__":
    ...