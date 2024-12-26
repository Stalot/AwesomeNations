from awesomeNations import AwesomeNations as awn

region = awn.Region

def get_embassies(region_name):
    print('\033[1m' + 'Getting Embassies...' + '\033[0m')
    data: dict = region(region_name).get_embassies()
    return data

# Generator to simulate data
def table_generator(data):
    for embassy in data['embassies']:
        yield (embassy['region'], embassy['duration'])

def main():
    region_name = str(input('Region name: '))
    region_name = region_name.strip()

    if not region_name:
        print('\033[0;31m' + '\nPlease, insert a region name!\n' + '\033[0m')
        main()
    elif not region(region_name).exists():
        print('\033[0;31m' + '\nRegion not found!\n' + '\033[0m')
        main()

    data: dict = get_embassies(region_name)

    if data['embassies'] == None:
        print('\033[0;31m' + '\nThese losers do not have embassies!\n' + '\033[0m')
        main()
    total = data['total']

    # Calculate the maximum width dynamically using a generator
    table_data = table_generator(data)
    max_width = max(len(row[0]) for row in table_data)

    # Re-create the generator since it gets exhausted after max_width calculation
    table_data = table_generator(data)

    # Print each row with aligned columns
    for left, right in table_data:
        print(left.ljust(max_width) + " | " + right)
    print('\033[1m' + f'Total: {total}' + '\033[0m\n')
    main()

if __name__ == "__main__":
    main()