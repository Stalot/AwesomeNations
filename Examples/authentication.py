from awesomeNations import AwesomeNations
from dotenv import load_dotenv
import os

#  █████╗ ██╗    ██╗███████╗███████╗ ██████╗ ███╗   ███╗███████╗
# ██╔══██╗██║    ██║██╔════╝██╔════╝██╔═══██╗████╗ ████║██╔════╝
# ███████║██║ █╗ ██║█████╗  ███████╗██║   ██║██╔████╔██║█████╗  
# ██╔══██║██║███╗██║██╔══╝  ╚════██║██║   ██║██║╚██╔╝██║██╔══╝  
# ██║  ██║╚███╔███╔╝███████╗███████║╚██████╔╝██║ ╚═╝ ██║███████╗
# ╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝ 

# In order to authenticate, you need to insert a password or autologin
# ⚠️ Don't store credentials in source code!
load_dotenv()
my_password = os.environ["MY_PASSWORD"]

api = AwesomeNations("AwesomeNations authentication example") # Replace this User-Agent with useful info.

# First way
nation = api.Nation("nation_name", my_password, "or autologin...")

# Second way
nation = api.Nation("nation_name")
nation.set_auth(my_password, "or autologin...")

# Third way
with api.Nation("nation_name") as n:
    n.set_auth(my_password, "or autologin...")