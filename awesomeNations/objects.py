from bs4 import BeautifulSoup as bs
from icecream import ic
from datetime import datetime
import requests

headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'}

today = datetime.today()
date = today.strftime('%H:%M:%S')
ic.configureOutput(prefix=f'{date} --> ')

class methods:
    def format(text: str) -> str:
        formatted_text = text.lower().replace(' ', '_')
        return formatted_text

def nationBubbles(top, bottom):
        bubble_keys = [methods.format(title.get_text()) for title in top]
        bubble_values = [key.get_text() for key in bottom]
        bubbles = {}

        for i in range(len(bubble_keys)):
            bubbles.update({bubble_keys[i]: bubble_values[i]})

        return bubbles

def summaryBox(box):
    items = [item.get_text() for item in box]
    population = items[1]
    capital = items[4]
    leader = items[6]
    faith = items[8]
    currency = items[11]
    animal = items[13]

    values = dict(population=population, capital=capital, leader=leader, faith=faith, currency=currency, animal=animal)
    return values

class Nation:
    def __init__(self, nation_name) -> None:
        self.nation_name = nation_name

    def check_if_nation_exists(nation_name: str) -> bool:
        """
        Checks if the nation exists by searching for its name.
        """

        html = html = requests.get(f'https://www.nationstates.net/nation={nation_name}/detail=trend/censusid={id}', headers=headers)
        soup = bs(html.text, 'html.parser')
        error_p = soup.find('p', class_="error")

        if error_p:
            return False
        else:
            return True

    def overview(nation_name = 'testlandia') -> dict:
        formatted_name = methods.format(nation_name)

        html = requests.get(f'https://www.nationstates.net/nation={formatted_name}', headers=headers)
        soup = bs(html.text, 'html.parser')

        flag_source = soup.find('div', class_='newflagcellbox').find('img')
        flag = f'www.nationstates.net{flag_source.attrs['data-cfsrc']}'

        short_name = soup.find('div', class_='newtitlename').get_text()
        long_name = f'{soup.find('div', class_='newtitlepretitle').get_text()} {short_name}'
        category = soup.find('div', class_='newtitlecategory').get_text()
        motto = soup.find('span', class_='slogan').get_text()

        bubble_top_line = soup.find_all('div', class_='newmainlinebubbletop')
        bubble_bottom_line = soup.find_all('div', class_='newmainlinebubblebottom')
        bubbles = nationBubbles(bubble_top_line, bubble_bottom_line)

        nationsummary = soup.find('div', class_='nationsummary').find_all('p')
        government = f'{nationsummary[0].get_text()}\n{nationsummary[1].get_text()}'
        economy = nationsummary[2].get_text()
        more = nationsummary[3].get_text()
        description = dict(government=government, economy=economy, more=more)

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