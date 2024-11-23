from awesomeNations import AwesomeNations as awn

if __name__ == '__main__':
    print('TESTING\n')

    def nation_search(nations):
        for nation in nations:
            data = awn.get_census(nation, [16, 17, 26, 46, 12], raw=True)

            nation_data = data[str(nation).lower().replace(' ', '_')]
            print(f"\n{nation}:\n")
            for item in nation_data:
                print(f"{str(item).replace('_', ' ')}: {nation_data[item]}")
    
    #nation_search(['ponytus', 'orlys', 'neo-democratic Kolokia'])