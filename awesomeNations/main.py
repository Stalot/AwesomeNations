from bs4 import BeautifulSoup as bs
from .exceptions import InvalidQuery, NationException
import requests

headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'}


def check_if_nation_exists(nation_name: str):
    html = html = requests.get(f'https://www.nationstates.net/nation={nation_name}/detail=trend/censusid={id}', headers=headers)
    soup = bs(html.text, 'html.parser')
    error_p = soup.find('p', class_="error")

    if error_p:
        return False
    else:
        return True

class AwesomeNations:
    def __init__(self) -> None:
        pass

    def nation_exists(nation_name: str):
        return check_if_nation_exists(nation_name)

    def get_census(nation_name = 'testlandia', censusid = [0], raw = True):
        nation_name = str(nation_name).lower().replace(' ', '_')
        if type(censusid) is not list:
            raise InvalidQuery(censusid, censusid)

        exist = check_if_nation_exists(nation_name)
        if exist == True:
            data = {}
            nation_data = {}

            for id in censusid:
                id = int(id)
                if id < 88:
                    html = requests.get(f'https://www.nationstates.net/nation={nation_name}/detail=trend/censusid={id}', headers=headers)
                    soup = bs(html.text, 'html.parser')

                    if raw == False:
                        census_value = soup.find('div', class_='censusscoreboxtop').get_text().replace(',', '')
                        if '.' in census_value:
                            census_value = float(census_value)
                        else:
                            census_value = int(census_value)
                    else:
                        census_value = soup.find('div', class_='censusscoreboxtop').get_text().replace(' ', '')
                    census_name = str(soup.find('h2').findChild('a', class_ = 'quietlink').get_text().lower().replace(' ', '_').replace(':', ''))
                    data[census_name] = census_value
                else:
                    raise InvalidQuery(censusid, id)
                nation_data[nation_name] = data
        else:
            raise NationException(nation_name)
        return nation_data
    
    def one_plus_one():
        return 1 + 1