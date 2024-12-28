from awesomeNations import AwesomeNations as awn
from datetime import datetime

def get_date():
    date = datetime.today().strftime('%H:%M:%S')
    return date

print(get_date())
data = {}
data = awn.Nation('testlandia').get_census([id for id in range(0, 89)])
print(get_date())