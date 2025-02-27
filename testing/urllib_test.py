from urllib import request, parse
from awesomeNations.exceptions import HTTPError
from dotenv import load_dotenv
import os
from pprint import pprint as pp
import time

load_dotenv(".env")

calamity_password = os.environ["THE_HOSTS_OF_CALAMITY_PASSWORD"]

class Connection:
    def __init__(self, headers):
        self.base_api_url: str = "https://www.nationstates.net/cgi-bin/api.cgi"
        self.headers: dict = headers

    def urlib_request_url(self, url_params: dict[str, str]):
        querystring = parse.urlencode(url_params)
        url = self.base_api_url + "?" + querystring
        
        request_object = request.Request(url, None, headers=self.headers)
        response = request.urlopen(request_object)
        
        if self.headers["X-Autologin"] == "":
            self.headers.update({"X-Autologin": response.headers.get("X-Autologin", "")})
        print(self.headers["X-Autologin"])
        
        if response.code != 200:
            raise HTTPError(response.code)
        decoded_response = response.read().decode("UTF-8")
        return decoded_response

class Nation:
    def __init__(self,
                 nation_name: str = None,
                 password: str = None,
                 autologin: str = None):
        self.nation_name = nation_name
        self.password = password
        self.autologin = autologin
        
        headers = {"User-Agent": "Urllib connection test (by: Orlys)",
                   "X-Password": password if password else "",
                   "X-Autologin": autologin if autologin else ""}
        self.connection = Connection(headers)
        
    def get_data(self, shards: list[str] | tuple[str]) -> None:
        shards = "+".join(shards)
        params = {"nation": self.nation_name,
                  "q": shards}
        print(self.connection.urlib_request_url(params))

nation = Nation("The hosts of calamity", None, ".ovApudbiuWZyiVDkKxqXjg")
nation.get_data(["name", "dossier", "ping", "issues"])