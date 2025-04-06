from awesomeNations import AwesomeNations
import time
import tracemalloc

def speed_test(func):
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        t1 = time.time()
        func(*args, **kwargs)
        t2 = time.time()
        speed = round(t2 - t1, 2)
        memory = tracemalloc.get_traced_memory()
        print('\033[1;33m' + f'{func.__name__} took {speed} seconds to run\nMemory used: {round(memory[0] / 1e+6, 3)}Mb, peak: {round(memory[1] / 1e+6, 3)}Mb' + '\033[0m')
        tracemalloc.stop()
    return wrapper


api = AwesomeNations("AwesomeNations urllib3 test (by: Orlys; usdBy: Orlys)")

@speed_test
def do_request_in_quick_sucession_test():
    response: dict = api.Nation("Orlys").get_shards("name")
    return response

i = 10
while i > 1:
    do_request_in_quick_sucession_test()
    i -= 1