from awesomeNations import AwesomeNations as awn

region = awn.Region('The Pacific')

data = region.get_world_census([0, 8, 46])

for rank in data:
    print(f'{rank['title']}\n{rank['description']}\n')

    i = 1
    for nation in rank['rank']:
        print(f'{i}. {nation}')
        i += 1
    print('-'*100)