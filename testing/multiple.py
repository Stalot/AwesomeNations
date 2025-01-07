import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from awesomeNations.configuration import DEFAULT_HEADERS

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

def census_url_generator(nation_name: str, id: tuple):
      for id in id:
        yield f'https://www.nationstates.net/nation={nation_name}/detail=trend/censusid={id}'

# Define a function to scrape a single page
def scrape_page(url):
    try:
        response = requests.get(url, headers=DEFAULT_HEADERS, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract the desired data (adjust as needed)
        title = soup.find('h2').get_text()
        value = soup.find('div', class_='censusscoreboxtop').get_text().replace(' ', '')
        bubble_top_line = soup.find_all('div', class_='newmainlinebubbletop')
        bubble_bottom_line = soup.find_all('div', class_='newmainlinebubblebottom')
        bubbles = nationBubbles(bubble_top_line, bubble_bottom_line)
        
        return {'title': title, 'value': value, 'bubbles': bubbles}
    except Exception as e:
        return {url: f"Error: {e}"}

# List of URLs to scrape
urls = census_url_generator('orlys', (id for id in range(89)))

# Use ThreadPoolExecutor to scrape pages concurrently
def thread():
    with ThreadPoolExecutor(max_workers=100) as executor:  # Adjust the number of workers as needed
        futures = {executor.submit(scrape_page, url): url for url in urls}
        for future in futures:
            yield future.result()
results = thread()

# Print results
for result in results:
    print(result)
