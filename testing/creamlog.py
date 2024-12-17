from icecream import ic
from datetime import datetime

def configure(logging: bool = True):
    if logging:
        ic.enable()
    else:
        ic.disable()

    today = datetime.today()
    date = today.strftime('%H:%M:%S')
    ic.configureOutput(prefix=f'{date} --> ')

def log(log):
    ic(log)