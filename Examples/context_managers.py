from awesomeNations import AwesomeNations
from dotenv import load_dotenv
from pprint import pp
import os

#  █████╗ ██╗    ██╗███████╗███████╗ ██████╗ ███╗   ███╗███████╗
# ██╔══██╗██║    ██║██╔════╝██╔════╝██╔═══██╗████╗ ████║██╔════╝
# ███████║██║ █╗ ██║█████╗  ███████╗██║   ██║██╔████╔██║█████╗  
# ██╔══██║██║███╗██║██╔══╝  ╚════██║██║   ██║██║╚██╔╝██║██╔══╝  
# ██║  ██║╚███╔███╔╝███████╗███████║╚██████╔╝██║ ╚═╝ ██║███████╗
# ╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝ Isn't it?

# Get sensitive data from .env file
load_dotenv()
nation1_password = os.environ["MY_PASSWORD"]
nation2_password = os.environ["MY_PASSWORD2"]

api = AwesomeNations("AwesomeNations 2.1.0 - context managers example") # Replace this User-Agent with useful info.
nation = api.Nation

with nation("nation-1") as n:
    n.set_auth(nation1_password)
    data = n.get_shards("ping")
    pp(data)

with nation("nation-2") as n:
    n.set_auth(nation2_password)
    data = n.get_shards("ping")
    pp(data)

with api.Region("The Middle Pacific") as pacific:
    data = pacific.get_shards("officers")
    pp(data)