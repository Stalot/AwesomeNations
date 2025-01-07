from awesomeNations import AwesomeNations as awn

nation = awn.Nation('testlandia')

AwesomeData = nation.get_census((0, 2, 4, 46, 88)) # Returns a generator object

for census in AwesomeData:
    print(census)