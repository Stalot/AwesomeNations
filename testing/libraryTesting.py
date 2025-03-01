from awesomeNations import AwesomeNations
from pprint import pprint as pp # Normal printing, but more pretty!

awn = AwesomeNations("AwesomeNations/Test")

nation = awn.Nation
censuses = nation("unirstate").get_shards("census", scale="all", mode="score")
pp(censuses)