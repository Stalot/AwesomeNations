from awesomeNations import AwesomeNations as awn
from awesomeNations.seleniumScrapper import script_runner, get_dynamic_source
import time
import tracemalloc

def speed_test(func):
    def wrapper():
        tracemalloc.start()
        t1 = time.time()
        func()
        t2 = time.time()
        speed = round(t2 - t1, 2)
        memory = tracemalloc.get_traced_memory()
        print('\033[1;33m' + f'{func.__name__} took {speed} seconds to run\nMemory used: {round(memory[0] / 1e+6, 3)}Mb, peak: {round(memory[1] / 1e+6, 3)}Mb' + '\033[0m')
        tracemalloc.stop()
    return wrapper

@speed_test
def js_runner():
    source = script_runner('https://www.nationstates.net/page=activity/view=nation.orlys/filter=all', '//*[@id="loggedout"]/script[13]')

@speed_test
def dynamic_source():
    source = get_dynamic_source('https://www.nationstates.net/page=activity/view=nation.orlys/filter=all', '//*[contains(concat( " ", @class, " " ), concat( " ", "divindent", " " ))] | //*[contains(concat( " ", @class, " " ), concat( " ", "mcollapse", " " ))]')

js_runner()
dynamic_source()