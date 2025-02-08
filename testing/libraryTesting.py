from awesomeNations import AwesomeNations
from pprint import pprint as pp # Normal printing, but more pretty!

awn = AwesomeNations("My cute app/0.0.1")

region = awn.Region
region_shards = region("The EAST pacific").get_shards()
pp(region_shards, depth=2)