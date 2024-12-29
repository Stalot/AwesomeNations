from awesomeNations.exceptions import HTTPError, NationNotFound, CensusNotFound
from awesomeNations.configuration import DEFAULT_HEADERS, DEFAULT_PARSER
import requests
from bs4 import BeautifulSoup as bs
from typing import Iterator
from concurrent.futures import ThreadPoolExecutor

def request(parser: str = DEFAULT_PARSER, url: str = 'https://www.nationstates.net/'):
        html = requests.get(url, headers=DEFAULT_HEADERS)
        if html.status_code != 200:
                raise HTTPError(html.status_code)
        soup = bs(html.text, parser)
        response = {'bs4_soup': soup}
        return response

def format_text(text: str) -> str:
    formatted_text = text.lower().strip().replace(' ', '_')
    return formatted_text

def nationBubbles(top, bottom) -> dict:
        bubble_keys = [format_text(title.get_text()) for title in top]
        bubble_values = [key.get_text() for key in bottom]
        bubbles = {}

        for i in range(len(bubble_keys)):
            bubbles.update({bubble_keys[i]: bubble_values[i]})

        return bubbles

def census_url_generator(nation_name: str, id: tuple) -> Iterator:
      for id in id:
        yield f'https://www.nationstates.net/nation={nation_name}/detail=trend/censusid={id}'

def scrape_census(url: str) -> dict:
    try:
        response = requests.get(url, headers=DEFAULT_HEADERS, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        soup = bs(response.text, 'html.parser')
        # Extract the desired data (adjust as needed)
        title = soup.find('h2').get_text()
        value = soup.find('div', class_='censusscoreboxtop').get_text().replace(' ', '')
        bubble_top_line = soup.find_all('div', class_='newmainlinebubbletop')
        bubble_bottom_line = soup.find_all('div', class_='newmainlinebubblebottom')
        bubbles = nationBubbles(bubble_top_line, bubble_bottom_line)
        
        return {'title': title, 'value': value, 'bubbles': bubbles}
    except Exception as e:
        return {url: f"Error: {e}"}

# Use ThreadPoolExecutor to scrape pages concurrently
def census_generator(nation_name: str, censusid: tuple):
    urls = census_url_generator('orlys', (id for id in range(9)))
    with ThreadPoolExecutor(max_workers=100) as executor:  # Adjust the number of workers as needed
        futures = {executor.submit(scrape_census, url): url for url in urls}
        for future in futures:
            yield future.result()

a = census_generator()
for item in a:
     print(item)