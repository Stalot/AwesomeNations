from awesomeNations.exceptions import NationNotFound, CensusNotFound, HTTPError, RegionNotFound
from awesomeNations.configuration import DEFAULT_HEADERS, DEFAULT_PARSER
from bs4 import BeautifulSoup as bs
from awesomeNations.seleniumScrapper import get_dynamic_source
import requests

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

# Nation actions:
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

def census_urls(nation_name: str, ids: list) -> list:
    urls: list = []
    for id in ids:
        if not type(id).is_integer(id) or id > 88:
            raise CensusNotFound(id)
        current_url: str = f'https://www.nationstates.net/nation={nation_name}/detail=trend/censusid={id}'
        urls.append(current_url)
    return urls

def check_if_nation_exists(nation_name: str) -> None:
    url: str = f'https://www.nationstates.net/nation={nation_name}'
    response: dict = request(parser='html.parser', url=url)
    soup: bs = response['bs4_soup']
    error_p = soup.find('p', class_="error")

    if error_p:
        raise NationNotFound(nation_name)

class NationObject:
    def __init__(self, nation_name: str):
        self.nation_name = nation_name

    def exists(self) -> bool:
        nation_name: str = self.nation_name
        url: str = f'https://www.nationstates.net/nation={nation_name}'
        response: dict = request(parser='html.parser', url=url)
        soup: bs = response['bs4_soup']
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
        response: dict = request(parser='lxml', url=url)
        soup: bs = response['bs4_soup']

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

    def census(self, censusid: list) -> dict:
        nation_name: str = self.nation_name
        formatted_name = format_text(nation_name)
        check_if_nation_exists(formatted_name)

        urls = census_urls(formatted_name, censusid)

        census = {}

        for url in urls:
            response: dict = request(parser=DEFAULT_PARSER, url=url)
            soup: bs = response['bs4_soup']

            title = soup.find('h2').get_text()
            raw_value = soup.find('div', class_='censusscoreboxtop').get_text().replace(' ', '')
            formatted_value = float(raw_value.replace(',', ''))

            bubble_top_line = soup.find_all('div', class_='newmainlinebubbletop')
            bubble_bottom_line = soup.find_all('div', class_='newmainlinebubblebottom')
            bubbles = nationBubbles(bubble_top_line, bubble_bottom_line)

            if formatted_value.is_integer():
                formatted_value = int(formatted_value)

            census[format_text(title).replace(':', '')] = {
                'title': title,
                'raw_value': raw_value,
                'value': formatted_value,
                'bubbles': bubbles
                }

        return census

# Region actions:
def check_if_region_exists(region_name: str) -> None:
    url: str = f'https://www.nationstates.net/region={region_name}'
    response: dict = request(parser='html.parser', url=url)
    soup: bs = response['bs4_soup']
    error_p = soup.find('p', class_="error")

    if error_p:
        raise RegionNotFound(region_name)

def embassy(divindents: bs, default_output: dict) -> dict:
    embassy_section: bs = divindents[3].find('table', class_='shiny wide embassies mcollapse')

    if not embassy_section:
        return default_output

    embassy_names: list = [name.get_text() for name in embassy_section.find_all('td', class_='bigleft')]
    embassy_formatted_names: list = []
    for name in embassy_names:
        if str(name[0]).isnumeric():
            split: list = name.split(' ')
            split.pop(0)
            new_name = ' '.join(split)
            embassy_formatted_names.append(new_name)
        else:
            embassy_formatted_names.append(name)
        
    embassy_durations = [duration.get_text() for duration in embassy_section.find_all('td', class_='')]

    embassies = []

    for i in range(len(embassy_names)):
        if 'Closing' in embassy_durations[i]:
            embassy_durations[i] = embassy_durations[i].replace('Closing', ' Closing')
        embassies.append({'region': embassy_formatted_names[i], 'duration': embassy_durations[i]})

    embassies_dict = {'total': len(embassies), 'embassies': embassies}
    return embassies_dict

class RegionObject:
    def __init__(self, region_name: str):
        self.region_name = region_name
    
    def exists(self) -> bool:
        region_name: str = self.region_name
        url: str = f'https://www.nationstates.net/region={region_name}'
        response: dict = request(parser='lxml', url=url)
        soup: bs = response['bs4_soup']
        error_p = soup.find('p', class_="error")

        if error_p:
            return False
        else:
            return True

    def overview(self):
        region_name: str = self.region_name
        formatted_name: str = format_text(region_name)
        check_if_region_exists(formatted_name)

        url: str = f'https://www.nationstates.net/region={formatted_name}'
        response: dict = request(parser='lxml', url=url)
        soup: bs = response['bs4_soup']

        founder: str = None
        governor: str = None
        category: str = None
        wa_delegate: str = None
        last_wa_update: str = None
        region_flag: str = None
        region_banner: str = None

        region_cover = soup.find('div', class_='regioncover')

        flag_cover = region_cover.find('img')
        if flag_cover:
            if flag_cover.has_attr('src'):
                region_flag = f'https://www.nationstates.net{flag_cover.attrs['src']}'
            elif flag_cover.has_attr('data-cfsrc'):
                region_flag = f'https://www.nationstates.net{flag_cover.attrs['data-cfsrc']}'
        banner_source = region_cover.attrs['style'].replace('background-image:url', '').replace('(', '').replace(')', '')
        region_banner = f'https://www.nationstates.net{banner_source}'

        region_content = soup.find('div', id='regioncontent')
        paragraphs: list = region_content.find_all('p', limit=4)
        for text in paragraphs:
            content: str = text.get_text().strip()
            if 'Feeder' in content or 'Sinker' in content or 'Frontier' in content:
                category = content
            if 'Last WA Update' in content:
                last_wa_update = content
            if 'Governor' in content:
                governor = content
            if 'WA Delegate' in content:
                wa_delegate = content
            if 'Founder' in content:
                founder = content

        overview = dict(category=category, governor=governor, wa_delegate=wa_delegate, last_wa_update=last_wa_update, founder=founder, region_flag=region_flag, region_banner=region_banner)
        return overview

    def world_census(self, censusid: int) -> dict:
        region_name: str = self.region_name
        formatted_name: str = format_text(region_name)
        check_if_region_exists(formatted_name)

        url: str = f'https://www.nationstates.net/page=list_nations/censusid={censusid}/region={formatted_name}'
        
        response = request(parser='lxml', url=url)
        soup: bs = response['bs4_soup']

        #region_rank: dict = {}
        region_rank: list = []

        rank_table = soup.find('table', class_='shiny ranks nationranks mcollapse').find_all('tr')
        rank_table.pop(0)

        rank_elements = [td.find_all('td', limit=2) for td in rank_table]
        #rank_positions: list = []
        #rank_nations: list = []
        for td in rank_elements:
            #position = td[0].get_text().replace('.', '')
            nation = td[1].get_text()
            #rank_positions.append(position)
            #rank_nations.append(nation)
            region_rank.append(nation)

        #for i in range(len(rank_positions)):
        #    region_rank.update({rank_positions[i]: rank_nations[i]})
        
        page = soup.find('div', id='regioncontent')
        paragraphs = page.find_all('p', limit=2)

        description: str = paragraphs[0].get_text()
        region_world_rank: str = paragraphs[1].get_text()

        world_census: dict = {'title': page.find('h3').get_text(),
                              'description': description,
                              'region_world_rank': region_world_rank,
                              'rank': region_rank
                              }
        
        return world_census

    def activity(self, filter: str):
        region_name: str = self.region_name
        formatted_name: str = format_text(region_name)
        check_if_region_exists(formatted_name)

        url: str = f'https://www.nationstates.net/page=activity/view=region.{formatted_name}/filter={filter}'
        source: str = get_dynamic_source(url, '//*[@id="reports"]/ul')

        if source == None:
            events = 'No results.'
            ic(events)
            return events
        
        soup: bs = bs(source, DEFAULT_PARSER)
        reports = soup.find('div', class_='clickabletimes').find('ul')
        events = [li.get_text() for li in reports.find_all('li')]
        return events

    def embassies(self) -> dict:
        region_name: str = self.region_name
        formatted_name: str = format_text(region_name)
        check_if_region_exists(formatted_name)

        default_embassies_output: dict = {'total': 0, 'embassies': None}

        url: str = f'https://www.nationstates.net/page=region_admin/region={formatted_name}'
        source: str = get_dynamic_source(url, '//*[contains(concat( " ", @class, " " ), concat( " ", "divindent", " " ))] | //*[contains(concat( " ", @class, " " ), concat( " ", "mcollapse", " " ))]')

        if source:
            soup: bs = bs(source, DEFAULT_PARSER)

            divindents = soup.find_all('div', class_='divindent')

            embassies: dict = embassy(divindents, default_embassies_output)
            return embassies
        return default_embassies_output