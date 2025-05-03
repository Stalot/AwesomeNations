from awesomeNations import AwesomeNations
from dotenv import load_dotenv
from datetime import datetime
from pprint import pp
import os
import calendar

#  █████╗ ██╗    ██╗███████╗███████╗ ██████╗ ███╗   ███╗███████╗
# ██╔══██╗██║    ██║██╔════╝██╔════╝██╔═══██╗████╗ ████║██╔════╝
# ███████║██║ █╗ ██║█████╗  ███████╗██║   ██║██╔████╔██║█████╗  
# ██╔══██║██║███╗██║██╔══╝  ╚════██║██║   ██║██║╚██╔╝██║██╔══╝  
# ██║  ██║╚███╔███╔╝███████╗███████║╚██████╔╝██║ ╚═╝ ██║███████╗
# ╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝ 

# Get sensitive data from .env file
load_dotenv()
password = os.environ["MY_PASSWORD"]

api = AwesomeNations("My application/1.0.0", # Replace this User-Agent with useful info.
                     allow_beta=True)
nation = api.Nation("your nation name here!", password)

def get_time() -> str:
    """
    Generates a pretty timestamp string based on the current time.
    
    Example:
    ```
    "13:37:09 on May 03, 2025."
    ```
    """
    today = datetime.today()
    month_name: str = calendar.month_name[today.month]
    return f"{today.strftime(f"%H:%M:%S on {month_name} %d, %Y")}."

# Make a dispatch:
response = nation.dispatch("add",
                           title="My awesome dispatch made with AwesomeNations",
                           text=f"This dispatch was made using AwesomeNations 2.1.0, at {get_time()}",
                           category=1,
                           subcategory=100)
pp(response) # Command response