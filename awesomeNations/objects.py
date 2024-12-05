from awesomeNations.exceptions import NationNotFound, InvalidQuery
from bs4 import BeautifulSoup as bs
from icecream import ic
from datetime import datetime
import requests

headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'}

today = datetime.today()
date = today.strftime('%H:%M:%S')
ic.configureOutput(prefix=f'{date} --> ', includeContext=True)

class methods:
    def format(text: str) -> str:
        formatted_text = text.casefold().replace(' ', '_')
        return formatted_text

def nationBubbles(top, bottom) -> dict:
        bubble_keys = [methods.format(title.get_text()) for title in top]
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

def census_urls(nation_name: str, ids: list) -> list:
    urls = []
    for id in ids:
        current_url = f'https://www.nationstates.net/nation={nation_name}/detail=trend/censusid={id}'
        urls.append(current_url)
    return urls

class NationObject:
    def exists(nation_name: str) -> bool:
        html = requests.get(f'https://www.nationstates.net/nation={nation_name}', headers=headers)
        soup = bs(html.text, 'html.parser')
        error_p = soup.find('p', class_="error")

        if error_p:
            return False
        else:
            return True

    def overview(nation_name: str) -> dict:
        formatted_name = methods.format(nation_name)

        html = requests.get(f'https://www.nationstates.net/nation={formatted_name}', headers=headers)
        soup = bs(html.text, 'lxml')

        flag_source = soup.find('div', class_='newflagbox').find('img').extract()
        if flag_source.has_attr('src'):
            flag = f'www.nationstates.net{flag_source.attrs['src']}'
        elif flag_source.has_attr('data-cfsrc'):
            flag = f'www.nationstates.net{flag_source.attrs['data-cfsrc']}'

        short_name = soup.find('div', class_='newtitlename').get_text().replace('\n', '')
        long_name = f'{soup.find('div', class_='newtitlepretitle').get_text()} {short_name}'.replace('\n', '')
        category = soup.find('div', class_='newtitlecategory').get_text()
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
                    'category': category,
                    'motto': motto,
                    'bubbles': bubbles,
                    'description': description,
                    'box': box
                    }

        ic(overview)
        return overview

    def census(nation_name: str, censusid: list) -> dict:
        formatted_name = methods.format(nation_name)
        urls = census_urls(formatted_name, censusid)

        census = {}

        for url in urls:
            html = requests.get(url, headers=headers)
            soup = bs(html.text, 'html.parser')

            title = soup.find('h2').get_text()
            raw_value = soup.find('div', class_='censusscoreboxtop').get_text().replace(' ', '')
            formatted_value = float(raw_value.replace(',', ''))

            bubble_top_line = soup.find_all('div', class_='newmainlinebubbletop')
            bubble_bottom_line = soup.find_all('div', class_='newmainlinebubblebottom')
            bubbles = nationBubbles(bubble_top_line, bubble_bottom_line)

            if formatted_value.is_integer():
                formatted_value = int(formatted_value)

            census[methods.format(title)] = {
                'title': title,
                'raw_value': raw_value,
                'value': formatted_value,
                'bubbles': bubbles
                }

        ic(census)
        return census