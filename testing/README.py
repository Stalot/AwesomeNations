from awesomeNations import AwesomeNations as awn

region = awn.Region
rank = region("The Pacific").get_world_census(censusid=46)
print(rank)