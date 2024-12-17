from awesomeNations import AwesomeNations as awn
from creamlog import configure, log

configure()

if __name__ == '__main__':
    print('OVERVIEW TESTING\n')
    mynation = awn.Nation('Testlandia')
    data = mynation.get_overview()

    #print(f'{data['short_name']}\n{data['long_name']}')
    log(data)