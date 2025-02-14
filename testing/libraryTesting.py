from awesomeNations import AwesomeNations
from pprint import pprint as pp # Normal printing, but more pretty!

awn = AwesomeNations("My cute app/0.0.1")

nation = awn.Nation
censuses = nation("unirstate").get_public_shards("census", scale="76")
pp(censuses)