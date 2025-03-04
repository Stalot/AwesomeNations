from awesomeNations.customObjects import AwesomeParser, Authentication
from awesomeNations.customMethods import join_keys
from awesomeNations.exceptions import HTTPError
from typing import Optional, Literal
from pprint import pprint as pp
from dotenv import load_dotenv
from pathlib import Path
import urllib3
import logging
import urllib
import time
import os

logger = logging.getLogger("AwesomeLogger")
logging.basicConfig(level=logging.WARNING, format="[%(asctime)s] %(levelname)s: %(message)s")

parser = AwesomeParser()

class WrapperConnection():
    def __init__(self,
                 headers: dict = None,
                 ratelimit_sleep = True,
                 ratelimit_reset_time = 30,
                 api_version = 12,
                 ):
        self.headers: dict = headers
        self.request_timeout: int | tuple = 10
        self.ratelimit_sleep: int = ratelimit_sleep
        self.ratelimit_reset_time: int = ratelimit_reset_time
        self.ratelimit_remaining: int = None
        self.api_version: int = api_version
        
        self.pool_manager = urllib3.PoolManager(4, self.headers)
        
        self.last_request_headers: dict = {}
        self.auth: Optional[Authentication] = None

    def fetch_api_data(self,
                       url: str = 'https://www.nationstates.net/',
                       query_parameters: Optional[dict] = None) -> dict:
        """
        This fetches API data and automatically parses it: (xml response -> python dictionary)
        """
        url = url.format(v=self.api_version)
        
        # Updates headers X-Password, X-Autologin and X-Pin in the next request
        # for actions that need authentication (Like private shards).
        if self.auth:
            self.headers.update(self.auth.get())

        response = self.pool_manager.request("GET", url, headers=self.headers, fields=query_parameters, timeout=self.request_timeout)

        if response.status != 200:
            raise HTTPError(response.status)
        
        self.last_request_headers.update(response.headers)
        x_pin_header: int | None = response.headers.get("X-Pin")
        
        # Updates self.auth X-Pin if necessary (for quick sucessive requests):
        if self.auth and x_pin_header:
            if self.auth.xpin != x_pin_header:
                self.auth.xpin = x_pin_header
        
        ratelimit_remaining: str | None = response.headers.get("Ratelimit-remaining")
        self.ratelimit_remaining = int(ratelimit_remaining) if ratelimit_remaining else None
        self.api_ratelimit()

        parsed_response = parser.parse_xml(response.data.decode())
        return parsed_response

    def fetch_file(self,
                   url: str,
                   filepath: str | Path) -> None:
        "Dowloads a file"
        if not Path(filepath).suffix:
            raise ValueError(f"{filepath}: This path needs a suffix dude!")
        with self.pool_manager.request("GET", url, preload_content=False) as file_response, open(filepath, "wb") as file_out:
            for chunk in file_response.stream(10**4, True):
                file_out.write(chunk)

    def connection_status_code(self, url: str = 'https://www.nationstates.net/') -> int:
        response = self.pool_manager.request("GET", url, headers=self.headers, timeout=20)
        
        self.last_request_headers.update(response.headers)

        ratelimit_remaining: str | None = response.headers.get("Ratelimit-remaining")
        self.ratelimit_remaining = int(ratelimit_remaining) if ratelimit_remaining else None
        self.api_ratelimit()

        return response.status
   
    def api_ratelimit(self) -> None:
        """
        Checks the NationStates API ratelimit and hibernates if the request limit was reached.
        """
        if self.ratelimit_remaining:
            if self.ratelimit_remaining <= 1:
                logger.warning(f"API ratelimit reached, your code will be paused for: {self.ratelimit_reset_time} seconds.")
                time.sleep(self.ratelimit_reset_time + 1)
                logger.info("Hibernation finished")

class URLManager():
    def __init__(self, api_base_url: str):
        self.api_base_url = api_base_url
    
    def generate_shards_url(self,
                    modifier: Literal["nation", "region", "world", "wa"],
                    shards: Optional[str | tuple[str]] = None,
                    params: Optional[str | tuple[str]] = None,
                    **kwargs) -> str:
        """
        Generates urls for shards, returns the standard API structure if no shards provided (if supported).
        """
        querystring: str = None
        match modifier:
            case "nation":
                querystring = f"nation={kwargs["nation_name"]}&q="
                if not shards:
                    querystring = querystring.replace("&q=", "")
            case "region":
                querystring = f"region={kwargs["region_name"]}&q="
                if not shards:
                    querystring = querystring.replace("&q=", "")
            case "world":
                querystring = "q="
                if not shards:
                    raise ValueError(f"Shards cannot be None, World API modifier needs shards!")
            case "wa":
                querystring = f"wa={kwargs["council_id"]}&q="
                if not shards:
                    raise ValueError(f"Shards cannot be None, World Assembly API modifier needs shards!")
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
        full_url: str = self.api_base_url + "?" + querystring + "&v={v}"
        return full_url

if __name__ == "__main__":
    headers = {"User-Agent": "AwesomeNations urllib3 test (by: Orlys; usdBy: Orlys)"}
    wrapper = WrapperConnection(headers, request_timeout=8)
    url_manager = URLManager("https://www.nationstates.net/cgi-bin/api.cgi")
    
    load_dotenv(".env")
    
    wrapper.auth = Authentication(os.environ["CALAMITY_PASSWORD"])
    
    url = url_manager.generate_shards_url("nation",
                                          ("fullname", "religion", "flag", "leader"),
                                          None,
                                          nation_name="Orlys",
                                          api_version=12)
    
    print(url)
    print(wrapper.request_timeout)
    
    def do_request_in_quick_sucession_test(url):
        response: dict = wrapper.fetch_api_data(url)
        return response
    
    pp(do_request_in_quick_sucession_test(url))