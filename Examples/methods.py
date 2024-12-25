from awesomeNations import AwesomeNations as awn

nation_name = 'testlandia'
region_name = 'the pacific'

nation = awn.Nation
region = awn.Region

print('NATION:')
# Returns True or False
print(f'{nation(nation_name).exists() = }\n')

# Returns a dictionary with short name, long name, WA category, motto and etc.
print(f'{nation(nation_name).get_overview() = }\n')

# Returns a dictionary containing the nation censuses, like: Title, (region/world rank), value and etc.
print(f'{nation(nation_name).get_census([46]) = }\n')

print('REGION:')
# Returns True or False
print(f'{region(region_name).exists() = }\n')

# Returns a dictionary with governor, WA delegate, founder, region_banner and etc.
print(f'{region(region_name).get_overview() = }\n')

# Returns a dictionary too: Title, description, nation rank (list) and more.
print(f'{region(region_name).get_world_census(46) = }\n')

# You know the drill. Returns the total number of embassies, their region and duration.
print(f'{region(region_name).get_embassies() = }\n')