from awesomeNations import AwesomeNations as awn

nation = 'testlandia'

def get_nation_data(nation: str):
    # Verifies if nation exists:
    exists = awn.nation_exists(nation)

    if exists:
        # Getting nation census (0-88):
        raw_data = awn.get_census(nation, [46, 74])
        print(f'Raw: {raw_data}')

        # Changing the "raw" argument (True by default):
        data = awn.get_census(nation, [46, 74], raw=False)
        print(f'Formatted: {data}')
    else:
        print(f'"{nation}" not found.')

if __name__ == '__main__':
    get_nation_data(nation)