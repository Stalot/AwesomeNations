from awesomeNations.configuration import DEFAULT_HEADERS

# Browser automation modules
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.firefox import GeckoDriverManager 

def driver_setup():
    # Automatically installs the current browser version
    service = Service (GeckoDriverManager().install())

    options = Options()
    options.add_argument("--headless")
    options.add_argument(F"--user-agent={DEFAULT_HEADERS}")

    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Wait until element x is present and then get the page source.
def get_dynamic_source(url: str, xpath: str):
    driver = driver_setup()
    driver.get(url)
    try:
        wait = WebDriverWait(driver, 5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

        source = None
        if element.is_displayed():
            source = driver.page_source
        return source
    except:
        return None
    finally:
        driver.quit()

def script_runner(url: str, script_xpath: str):
    driver = driver_setup()
    driver.get(url)
    try:
        driver.execute_script(script_xpath)
        source = driver.page_source
        return source
    except TimeoutException:
        return None
    finally:
        driver.quit()

if __name__ == "__main__":
    get_dynamic_source('https://www.nationstates.net/page=region_admin/region=fullworthia', '//*[contains(concat( " ", @class, " " ), concat( " ", "divindent", " " ))] | //*[contains(concat( " ", @class, " " ), concat( " ", "mcollapse", " " ))]')
    print('get_dynamic_source completed')

    script_runner('https://www.nationstates.net/page=activity/view=nation.democratic_fun', '//*[@id="loggedout"]/script[13]')
    print('script_runner completed')