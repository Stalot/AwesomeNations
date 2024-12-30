from awesomeNations.exceptions import NationNotFound
from bs4 import BeautifulSoup as bs
from awesomeNations.sharedMethods import request, format_text
from typing import Iterator
from concurrent.futures import ThreadPoolExecutor
from awesomeNations.configuration import DEFAULT_PARSER
import csv

def nationBubbles(top, bottom) -> dict:
        bubble_keys = [format_text(title.get_text()) for title in top]
        bubble_values = [key.get_text() for key in bottom]
        bubbles = {}

        for i in range(len(bubble_keys)):
            bubbles.update({bubble_keys[i]: bubble_values[i]})

        return bubbles

def nationSummary(nationsummary) -> dict:
    government = f'{nationsummary[0].get_text()}\n{nationsummary[1].get_text()}'
    economy = nationsummary[2].get_text()
    more = nationsummary[3].get_text()
    description = dict(government=government, economy=economy, more=more)

    return description

def summaryBox(box) -> dict:
    items = [item.get_text() for item in box]
    population = items[items.index('Population') + 1] if 'Population' in items else '...'
    capital = items[items.index('Capital') + 1] if 'Capital' in items else '...'
    leader = items[items.index('Leader') + 1] if 'Leader' in items else '...'
    faith = items[items.index('Faith') + 1] if 'Faith' in items else '...'
    currency = items[items.index('Currency') + 1] if 'Currency' in items else '...'
    animal = items[items.index('Animal') + 1] if 'Animal' in items else '...'

    values = dict(population=population, capital=capital, leader=leader, faith=faith, currency=currency, animal=animal)
    return values

def census_url_generator(nation_name: str, id: tuple) -> Iterator:
      for censusid in id:
        if censusid > 88:
            raise ValueError(censusid)
        yield {'url': f'https://www.nationstates.net/nation={nation_name}/detail=trend/censusid={id}', 'id': id}

def scrape_census(census_data: dict) -> dict:
    try:
        response = request(url=census_data['url'])
        soup: bs = response

        title = soup.find('h2').get_text()
        value = soup.find('div', class_='censusscoreboxtop').get_text().replace(' ', '')
        bubble_top_line = soup.find_all('div', class_='newmainlinebubbletop')
        bubble_bottom_line = soup.find_all('div', class_='newmainlinebubblebottom')
        bubbles = nationBubbles(bubble_top_line, bubble_bottom_line)
        return {'id': census_data['id'], 'title': title, 'value': value, 'bubbles': bubbles}
    except:
        return None

def check_if_nation_exists(nation_name: str) -> None:
    url: str = f'https://www.nationstates.net/nation={nation_name}'
    response: dict = request(parser=DEFAULT_PARSER, url=url)
    soup: bs = response
    error_p = soup.find('p', class_="error")

    if error_p:
        raise NationNotFound(nation_name)

class N:
    def __init__(self, nation_name: str) -> None:
        self.nation_name = nation_name

    def exists(self) -> bool:
        nation_name: str = self.nation_name
        url: str = f'https://www.nationstates.net/nation={nation_name}'
        response = request(parser='html.parser', url=url)
        soup: bs = response
        error_p = soup.find('p', class_="error")

        if error_p:
            return False
        else:
            return True

    def overview(self) -> dict:
        nation_name: str = self.nation_name
        formatted_name = format_text(nation_name)
        check_if_nation_exists(formatted_name)

        url: str = f'https://www.nationstates.net/nation={formatted_name}'
        response = request(parser='lxml', url=url)
        soup: bs = response

        flag_source = soup.find('div', class_='newflagbox').find('img').extract()
        if flag_source:
            if flag_source.has_attr('src'):
                flag = f'www.nationstates.net{flag_source.attrs['src']}'
            elif flag_source.has_attr('data-cfsrc'):
                flag = f'www.nationstates.net{flag_source.attrs['data-cfsrc']}'

        short_name = soup.find('div', class_='newtitlename').get_text().replace('\n', '')
        long_name = f'{soup.find('div', class_='newtitlepretitle').get_text()} {short_name}'.replace('\n', '')
        wa_category = soup.find('div', class_='newtitlecategory').get_text()
        motto = soup.find('span', class_='slogan').get_text()

        bubble_top_line = soup.find_all('div', class_='newmainlinebubbletop')
        bubble_bottom_line = soup.find_all('div', class_='newmainlinebubblebottom')
        bubbles = nationBubbles(bubble_top_line, bubble_bottom_line)

        nationsummary = soup.find('div', class_='nationsummary').find_all('p')
        description = nationSummary(nationsummary)

        nationsummarybox = soup.find('div', class_='nationsummarybox').find_all('td')
        box = summaryBox(nationsummarybox)

        overview = {
                    'flag': flag,
                    'short_name': short_name,
                    'long_name': long_name,
                    'wa_category': wa_category,
                    'motto': motto,
                    'bubbles': bubbles,
                    'description': description,
                    'box': box
                    }

        return overview

    def census_generator(self, censusid_tuple: tuple) -> Iterator:
        nation_name: str = self.nation_name
        generator_data = census_url_generator(nation_name, (id for id in censusid_tuple))
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(scrape_census, census_data): census_data for census_data in generator_data}
            for future in futures:
                yield future.result()

if __name__ == '__main__':
    data = census_url_generator('aaa', [i for i in range(200)])

    for i in data:
        print(i)