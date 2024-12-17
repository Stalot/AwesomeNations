from awesomeNations.configuration import DEFAULT_HEADERS

# Browser automation modules
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager 

def driver_setup():
    # Automatically installs the current browser version
    service = Service (ChromeDriverManager().install())

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument(F"--user-agent={DEFAULT_HEADERS}")

    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Wait until element x is present and then get the page source.
def get_dynamic_source(url: str, xpath):
    "wait until element x is present and then get the page source"
    print(f'Dynamic Selenium required at: {url}')
    driver = driver_setup()
    driver.get(url)
    try:
        wait = WebDriverWait(driver, 6)
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        source = driver.page_source
        return source
    except TimeoutException:
        return None
    finally:
        driver.quit()

if __name__ == "__main__":
    src = get_dynamic_source('https://www.nationstates.net/page=activity/view=region.fullworthia/filter=all', '//*[@id="reports"]/ul')
    print(src)