from awesomeNations import AwesomeNations as awn

region = awn.Region

def get_data(region_name: str):
    embassies = region(region_name).get_embassies()
    return embassies

def main():
    print('Getting embassies...\n')
    region_name = 'The Pacific'
    embassies = get_data(region_name)

    i = 0
    count = 0
    for embassy in embassies:
        i += 1
        if not embassy:
            print('These losers do not have embassies!')
            break
        print(f'{i}. {embassy['region']}')
        count += 1
        if count >= 10:
            input('\033[0;31m' + '(...) ' + '\033[0m')
            count = 0

if __name__ == "__main__":
    main()