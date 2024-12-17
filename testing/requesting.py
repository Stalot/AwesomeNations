from bs4 import BeautifulSoup as bs
from awesomeNations.exceptions import RequestError
from awesomeNations.configuration import CONFIG_VARS, configure
from typing import Final
import requests

configure()

HEADERS: Final[str] = CONFIG_VARS['DEFAULT_HEADERS']
configure()

def request(parser: str = CONFIG_VARS['DEFAULT_PARSER'], url: str = 'https://www.nationstates.net/'):
        html = requests.get(url, headers=HEADERS)
        if html.status_code != 200:
                raise RequestError(html.status_code)
        soup = bs(html.text, parser)
        response = {'bs4_soup': soup}
        return response

response: dict = request()
soup: bs = response['bs4_soup']
print(soup.find('h2'))