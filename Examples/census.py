from awesomeNations import AwesomeNations
from pprint import pprint as pp # (Use this if you want your prints more pretty)

#  █████╗ ██╗    ██╗███████╗███████╗ ██████╗ ███╗   ███╗███████╗
# ██╔══██╗██║    ██║██╔════╝██╔════╝██╔═══██╗████╗ ████║██╔════╝
# ███████║██║ █╗ ██║█████╗  ███████╗██║   ██║██╔████╔██║█████╗  
# ██╔══██║██║███╗██║██╔══╝  ╚════██║██║   ██║██║╚██╔╝██║██╔══╝  
# ██║  ██║╚███╔███╔╝███████╗███████║╚██████╔╝██║ ╚═╝ ██║███████╗
# ╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝ Isn't it?

awesomeAPI = AwesomeNations("My ultra omega super blaster cool application")
nation = awesomeAPI.Nation("testlandia")

defense_forces = nation.get_public_shards("census", scale=46)
pp(defense_forces)

# If you want all censuses:
all_censuses = nation.get_public_shards("census", scale="all")
pp(all_censuses)