from awesomeNations import AwesomeNations
from pprint import pprint as pp # (Use this if you want your prints more pretty)

#  █████╗ ██╗    ██╗███████╗███████╗ ██████╗ ███╗   ███╗███████╗
# ██╔══██╗██║    ██║██╔════╝██╔════╝██╔═══██╗████╗ ████║██╔════╝
# ███████║██║ █╗ ██║█████╗  ███████╗██║   ██║██╔████╔██║█████╗  
# ██╔══██║██║███╗██║██╔══╝  ╚════██║██║   ██║██║╚██╔╝██║██╔══╝  
# ██║  ██║╚███╔███╔╝███████╗███████║╚██████╔╝██║ ╚═╝ ██║███████╗
# ╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝ Isn't it?

api = AwesomeNations("My application/1.0.0") # Replace this User-Agent with useful info.
nation = api.Nation("testlandia")

defense_forces = nation.get_shards("census", scale=46)
pp(defense_forces)

# If you want all censuses:
all_censuses = nation.get_shards("census", scale="all")
pp(all_censuses)