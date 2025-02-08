from awesomeNations import AwesomeNations
from pprint import pprint as pp # (Use this if you want your prints more pretty)

#  █████╗ ██╗    ██╗███████╗███████╗ ██████╗ ███╗   ███╗███████╗
# ██╔══██╗██║    ██║██╔════╝██╔════╝██╔═══██╗████╗ ████║██╔════╝
# ███████║██║ █╗ ██║█████╗  ███████╗██║   ██║██╔████╔██║█████╗  
# ██╔══██║██║███╗██║██╔══╝  ╚════██║██║   ██║██║╚██╔╝██║██╔══╝  
# ██║  ██║╚███╔███╔╝███████╗███████║╚██████╔╝██║ ╚═╝ ██║███████╗
# ╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝

awesomeAPI = AwesomeNations("My Awesome Application")

nation = awesomeAPI.Nation("Testlandia") # Our favorite test dummy!
region = awesomeAPI.Region("The Pacific") # This region is older than 10 YEARS! Can you belive that?

# NOTE: Nation and region names are automatically formatted, so "The Celtics" becomes "the%20celtics".

# Checking if nation exists:
if nation.exists():
    print("This nation exists!")
else:
    print("This nation doesn't exist!")

# This little trick here gets the description of the nation page!
summary = nation.get_summary()
pp(summary)

# If you want nation or region data, you can request shards, stuff like: ["leader", "name", "fullname", "religion", ...]
# By default, this method retrives the Standard API.
pp(nation.get_public_shards())
pp(region.get_shards("flag"))

# This method dowloads the daily data dumps.
awesomeAPI.get_daily_data_dumps(type="region")

# Same with nation and region shards thing.
wa_data = awesomeAPI.get_world_assembly_shards(1, "delegates")
pp(wa_data)
world_data = awesomeAPI.get_world_shards("numnations")
pp(world_data)

# Extremelly important methods:
age = awesomeAPI.get_nationstates_age()
print(age)
birthday = awesomeAPI.today_is_nationstates_birthday()
print(birthday)
# You don't want to forget one's birthday, do you? DO YOU?!