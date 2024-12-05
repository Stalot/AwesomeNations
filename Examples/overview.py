from awesomeNations import AwesomeNations as awn

nation = awn.Nation

def get_cool_data(nation_name: str = 'testlandia'):
    if nation(nation_name).exists():
        overview = nation(nation_name).get_overview()
        return overview
    else:
        return "Nation not found."

def main():
    nation_name = str(input('Nation name: '))
    data = get_cool_data(nation_name)
    if data != 'Nation not found.':
        print(f'{data['long_name']} is a wonderful nation!\n')
    else:
        print(f'{data}\n')
    main()

if __name__ == '__main__':
    main()