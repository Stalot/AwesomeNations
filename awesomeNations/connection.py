from awesomeNations.exceptions import HTTPError
from awesomeNations.customObjects import AwesomeParser, Authentication
from awesomeNations.customMethods import join_keys
import time
import urllib3
from urllib import parse
from pprint import pprint as pp
from typing import Optional
import os
from dotenv import load_dotenv

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

    def fetch_api_data(self,
                       url: str = 'https://www.nationstates.net/',
                       query_parameters: None = None,
                       stream: bool = False,
                       auth: Authentication = None) -> dict:
        url += f"&v={self.api_version}"
        
        if auth:
            self.request_headers.update(auth.get())
        
        response = urllib3.request("GET", url, headers=self.headers, timeout=self.request_timeout)

        if response.status != 200:
            raise HTTPError(response.status)
        
        self.request_headers.update(response.headers)
        
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
        Checks the NationStates API ratelimit and time sleeps the code if the request limit is reached.
        """
        if self.ratelimit_remaining and self.ratelimit_remaining <= 1:
            time.sleep(self.ratelimit_sleep + 1)

class URLManager():
    def __init__(self, api_base_url: str):
        #self.api_base_url: str = "https://www.nationstates.net/cgi-bin/api.cgi"
        self.api_base_url = api_base_url
    
    def generate_shards_url(self,
                     shards: Optional[str | tuple[str]] = None,
                     params: Optional[str | tuple[str]] = None) -> str:
        """
        Generates urls for shards, returns the standard API structure if no shards provided.
        """
        url = self.api_base_url + "?{}={}"
        if shards:
            query_shards: str = join_keys(shards) if type(shards) is not str else shards
            query_params: str = params
            full_query: str = query_shards + ";" + query_params if query_params else query_shards
            url += "&q=" + full_query
        return url.lower()

if __name__ == "__main__":
    wrapper = WrapperConnection({"User-Agent": "AwesomeNations urllib3 test (by: Orlys; usdBy: Orlys)"})
    url_manager = URLManager("https://www.nationstates.net/cgi-bin/api.cgi")
    
    load_dotenv(".env")
    
    kwargs = {}
    params: str | None = join_keys([f"{kwarg}={kwargs[kwarg]}" for kwarg in kwargs], ";") if kwargs else None
    shards = None
    
    url = url_manager.generate_shards_url(None, None)
    url = url.format("nation", "orlys")
    response = wrapper.fetch_api_data(url)