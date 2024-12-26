from awesomeNations import AwesomeNations as awn
from pprint import pprint as pp

nation_name = 'testlandia'
region_name = 'the allied nations'

nation = awn.Nation
region = awn.Region

print('NATION:')
# Returns True or False
print(f'{nation(nation_name).exists() = }')

print('\nNation overview:')
# Returns a dictionary with short name, long name, WA category, motto and etc.
pp(nation(nation_name).get_overview())

print('\nNation census:')
# Returns a dictionary containing the requested nation censuses, like: Title, region and world rank, value and etc.
pp(nation(nation_name).get_census([46]))


print('\nREGION:')
# Returns True or False
print(f'{region(region_name).exists() = }')

print('\nRegion overview:')
# Returns a dictionary with governor, WA delegate, founder, region_banner and etc.
pp(region(region_name).get_overview())

print('\nRegion world census:')
# Returns a dictionary too: Rank title, description, rank (Top 10 nations) and more.
pp(region(region_name).get_world_census(46))

print('\nRegion embassies:')
# You know the drill. Returns the total number of embassies, their region and duration.
pp(region(region_name).get_embassies())