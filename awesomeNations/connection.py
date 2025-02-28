import urllib.parse
from awesomeNations.exceptions import HTTPError
from awesomeNations.customObjects import AwesomeParser, Authentication
from awesomeNations.customMethods import join_keys
import time
import urllib3
from urllib import parse
import urllib
from pprint import pprint as pp
from typing import Optional, Literal
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger("AwesomeLogger")
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")

parser = AwesomeParser()

class WrapperConnection():
    def __init__(self,
                 headers: dict = None,
                 session: bool = False,
                 request_timeout: int | tuple = 10,
                 ratelimit_sleep = True,
                 ratelimit_reset_time = 30,
                 api_version = 12,
                 ):
        self.headers = headers
        self.session = session
        self.request_timeout = request_timeout
        self.ratelimit_sleep = ratelimit_sleep
        self.ratelimit_reset_time = ratelimit_reset_time
        self.ratelimit_remaining: int = None
        self.ratelimit_requests_seen: int = None
        self.api_version = api_version
        
        self.request_headers: dict = {}
        self.auth: Optional[Authentication] = None

    def fetch_api_data(self,
                       url: str = 'https://www.nationstates.net/',
                       query_parameters: None = None,
                       stream: bool = False) -> dict:
        url += f"&v={self.api_version}"
        
        if self.auth:
            self.headers.update(self.auth.get())
        
        response = urllib3.request("GET", url, headers=self.headers, timeout=self.request_timeout)

        if response.status != 200:
            raise HTTPError(response.status)
        
        self.request_headers.update(response.headers)
        self.headers.update({"X-Pin": response.headers["X-Pin"]}) if response.headers.get("X-Pin") else ...
        
        ratelimit_remaining: str | None = self.request_headers.get("Ratelimit-remaining")
        self.ratelimit_remaining = int(ratelimit_remaining) if ratelimit_remaining else None
        self.api_ratelimit()

        parsed_response = parser.parse_xml(response.data.decode())
        return parsed_response

    def connection_status_code(self, url: str = 'https://www.nationstates.net/') -> int:
        response = urllib3.request("GET", url, headers=self.headers, timeout=20)
        
        self.request_headers.update(response.headers)

        ratelimit_remaining: str | None = self.request_headers.get("Ratelimit-remaining")
        self.ratelimit_remaining = int(ratelimit_remaining) if ratelimit_remaining else None
        self.api_ratelimit()

        return response.status

    def api_ratelimit(self) -> None:
        """
        Checks the NationStates API ratelimit and hibernates if the request limit was reached.
        """
        if self.ratelimit_remaining:
            if self.ratelimit_remaining <= 1:
                logger.warning(f"API ratelimit reached, time delay: {self.ratelimit_reset_time} seconds.")
                time.sleep(self.ratelimit_reset_time + 1)
                logger.info("Hibernation finished")

class URLManager():
    def __init__(self, api_base_url: str):
        #self.api_base_url: str = "https://www.nationstates.net/cgi-bin/api.cgi"
        self.api_base_url = api_base_url
    
    def generate_shards_url(self,
                    modifier: Literal["nation", "region", "world", "wa"],
                    shards: str | tuple[str],
                    params: Optional[str | tuple[str]] = None) -> str:
        """
        Generates urls for shards, returns the standard API structure if no shards provided.
        """
        querystring: str = None
        match modifier:
            case "nation":
                querystring = "nation={}&q="
            case "region":
                querystring = "region={}&q="
            case "world":
                querystring = "q="
            case "wa":
                querystring = "wa={}&q="
            case _:
                raise ValueError(f"{modifier} is invalid. Modifier must be nation, region, world or wa.")

        shards_query: str = shards
        shards_params: str = params
        if shards:
            if type(shards) != str:
                shards_query = join_keys(shards)
                querystring += shards_query
        if params:
            if type(params) != str:
                shards_params: str = join_keys(params, ";")
                querystring += ";" +  shards_params
        full_url: str = self.api_base_url + "?" + querystring
        return full_url

if __name__ == "__main__":
    wrapper = WrapperConnection({"User-Agent": "AwesomeNations urllib3 test (by: Orlys; usdBy: Orlys)"})
    url_manager = URLManager("https://www.nationstates.net/cgi-bin/api.cgi")
    
    load_dotenv(".env")
    
    wrapper.auth = Authentication(os.environ["CALAMITY_PASSWORD"])
    
    url = url_manager.generate_shards_url("nation", None)
    url = url.format("fullworthia")
    print(url)
    
    def do_request_in_quick_sucession_test(url):
        response: dict = wrapper.fetch_api_data(url)
        return response
    
    #pp(do_request_in_quick_sucession_test(url))