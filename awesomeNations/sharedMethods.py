from awesomeNations.exceptions import HTTPError
from awesomeNations.configuration import DEFAULT_HEADERS, DEFAULT_PARSER
from bs4 import BeautifulSoup as bs
import requests

def request(parser: str = DEFAULT_PARSER, url: str = 'https://www.nationstates.net/') -> bs:
    try:
        html = requests.get(url, headers=DEFAULT_HEADERS, timeout=(10, 5))
        if html.status_code != 200:
            raise HTTPError(html.status_code)
        response = bs(html.text, parser)
        return response
    except TimeoutError:
        raise HTTPError(html.status_code)

def format_text(text: str) -> str:
    formatted_text = text.lower().strip().replace(' ', '_')
    return formatted_text