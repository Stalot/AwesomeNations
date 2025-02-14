from awesomeNations import AwesomeNations
from pprint import pprint as pp # Normal printing, but more pretty!

awn = AwesomeNations("My cute app/0.0.1")

nation = awn.Nation
censuses = nation("Nationuraniume Missile silo 37").get_public_shards("census", scale="all")
pp(censuses)