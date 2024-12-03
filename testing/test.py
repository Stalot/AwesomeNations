from awesomeNations import AwesomeNations as awn

if __name__ == '__main__':
    print('TESTING\n')
    data = awn.get_overview('fullworthia')
    print(data['short_name'])