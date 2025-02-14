from awesomeNations.exceptions import HTTPError
from awesomeNations.customObjects import AwesomeParser
import requests
import time

parser = AwesomeParser()

def check_nationstates_api_ratelimit(limit_remaining: int = None, reset_delay: int = None) -> None:
    """
    Checks the NationStates API ratelimit and time sleeps the code if the request limit is reached.
    """
    if limit_remaining <= 1:
        time.sleep(reset_delay + 1)

class WrapperConnection():
    def __init__(self,
                 request_headers: dict = None,
                 session: bool = False,
                 request_timeout: int | tuple = 10,
                 ratelimit_sleep = True,
                 ratelimit_reset_time = 30,
                 api_version = 12,
                 ):
        self.request_headers = request_headers
        self.session = session
        self.request_timeout = request_timeout
        self.ratelimit_sleep = ratelimit_sleep
        self.ratelimit_reset_time = ratelimit_reset_time
        self.ratelimit_remaining = None
        self.ratelimit_requests_seen = None
        self.api_version = api_version
        
        self.connectionSession = requests.Session()

    def fetch_api_data(self, url: str = 'https://www.nationstates.net/', query_parameters: None = None, stream: bool = False) -> dict:
        url += f"&v={self.api_version}"
        if self.session:
            response = self.connectionSession.get(url, headers=self.request_headers, timeout=self.request_timeout, stream=stream, params=query_parameters)
        else:
            response = requests.get(url, headers=self.request_headers, timeout=self.request_timeout, stream=stream, params=query_parameters)

        if response.status_code != 200:
            raise HTTPError(response.status_code)
        
        ratelimit_remaining: str | None = response.headers.get("Ratelimit-remaining")
        self.ratelimit_remaining = int(ratelimit_remaining) if ratelimit_remaining else None
        check_nationstates_api_ratelimit(self.ratelimit_remaining, self.ratelimit_reset_time)

        parsed_response = parser.parse_xml(response.text)
        return parsed_response

    def fetch_html_data(self, url: str = 'https://www.nationstates.net/', query_parameters: None = None, stream: bool = False) -> requests.Response:
        if self.session:
            response = self.connectionSession.get(url, headers=self.request_headers, timeout=self.request_timeout, stream=stream, params=query_parameters)
        else:
            response = requests.get(url, headers=self.request_headers, timeout=self.request_timeout, stream=stream, params=query_parameters)

        if response.status_code != 200:
            raise HTTPError(response.status_code)

        return response

    def test_api_connection(self, url: str = 'https://www.nationstates.net/') -> int:
        if self.session:
            response = self.connectionSession.get(url, headers=self.request_headers, timeout=20)
        else:
            response = requests.get(url, headers=self.request_headers, timeout=20)

        ratelimit_remaining: str | None = response.headers.get("Ratelimit-remaining")
        self.ratelimit_remaining = int(ratelimit_remaining) if ratelimit_remaining else None
        check_nationstates_api_ratelimit(self.ratelimit_remaining, self.ratelimit_reset_time)

        return response.status_code

class URLManager():
    def __init__(self, api_base_url: str):
        #self.api_base_url: str = "https://www.nationstates.net/cgi-bin/api.cgi"
        self.api_base_url = api_base_url
    
    def standard_url(self,
                 type: str = "n") -> str:
        url_result: str = None
        match type:
            case "n":
                url_result = self.api_base_url + "?nation={nation_name}"
            case "r":
                url_result = self.api_base_url + "?region={region_name}"
        
        return url_result
    
    def shards_url(self,
                   type: str = "n") -> str:
        """
        ## type: str
        
        ``` python
        "n" # {nation_name}, {query}, {params}.
        "r" # {region_name}, {query}, {params}.
        "w" # {query}, {params}.
        "wa" # {council_id}, {query}, {params}.
        ```
        """
        url_result: str = None
        match type:
            case "n":
                url_result = self.api_base_url + "?nation={nation_name}&q={query};{params}"
            case "r":
                url_result = self.api_base_url + "?region={region_name}&q={query};{params}"
            case "w":
                url_result = self.api_base_url + "?q={query};{params}"
            case "wa":
                url_result = self.api_base_url + "?wa={council_id}&q={query};{params}"

        return url_result

    def data_dumps_url(self,
                   type: str = "n") -> str:
        """
        ## type: str
        
        ``` python
        "n" # nation data dump.
        "r" # region data dump.
        "c" # trading cards data dump, {season_number}.
        ```
        """
        url_result: str = None
        match type:
            case "n":
                url_result = "https://www.nationstates.net/pages/nations.xml.gz"
            case "r":
                url_result = "https://www.nationstates.net/pages/regions.xml.gz"
            case "c":
                url_result = "https://www.nationstates.net/pages/cardlist_S{season_number}.xml.gz"

        return url_result

if __name__ == "__main__":
    pass