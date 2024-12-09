from awesomeNations import AwesomeNations as awn

if __name__ == '__main__':
    print('TESTING\n')
    mynation = awn.Nation('orlys')
    data = mynation.get_census([46, 88])
    census = data['defense_forces']
    print(f'{census['title']}\n{census['raw_value']}')