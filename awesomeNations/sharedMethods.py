from awesomeNations.exceptions import HTTPError
from awesomeNations.configuration import DEFAULT_HEADERS, DEFAULT_PARSER
from bs4 import BeautifulSoup as bs
import requests

def request(parser: str = DEFAULT_PARSER, url: str = 'https://www.nationstates.net/') -> bs:
    html = requests.get(url, headers=DEFAULT_HEADERS, timeout=10)
    if html.status_code != 200:
        raise HTTPError(html.status_code)
    response = bs(html.text, parser)
    return response

def format_text(text: str) -> str:
    formatted_text = text.lower().strip().replace(' ', '_')
    return formatted_text