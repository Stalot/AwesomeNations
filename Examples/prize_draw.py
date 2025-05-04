from awesomeNations import AwesomeNations
from dotenv import load_dotenv
from datetime import datetime
from pprint import pp
import os
import random

#  █████╗ ██╗    ██╗███████╗███████╗ ██████╗ ███╗   ███╗███████╗
# ██╔══██╗██║    ██║██╔════╝██╔════╝██╔═══██╗████╗ ████║██╔════╝
# ███████║██║ █╗ ██║█████╗  ███████╗██║   ██║██╔████╔██║█████╗  
# ██╔══██║██║███╗██║██╔══╝  ╚════██║██║   ██║██║╚██╔╝██║██╔══╝  
# ██║  ██║╚███╔███╔╝███████╗███████║╚██████╔╝██║ ╚═╝ ██║███████╗
# ╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝ 

# Get sensitive data from .env file
load_dotenv()
password = os.environ["MY_PASSWORD"]

api = AwesomeNations("Trading Card Prize example", # Replace this User-Agent with useful info.
                     allow_beta=True)
nation = api.Nation("your nation name here!")
region = api.Region("fullworthia")

def pretty_name(name: str) -> str:
    name = name.replace("_", " ").split(" ")
    name = [word.capitalize() for word in name]
    name = " ".join(name)
    return name

def grand_prize(card_id: int, card_season: int):
    region_data: dict = region.get_shards(("nations", "numnations"))["region"]
    nations: list = region_data["nations"].split(":")
    
    lucky_id = int(region_data["numnations"] * random.random())
    prize_winner: str = pretty_name(nations[lucky_id])
    
    print("winner:", prize_winner)
    
    nation.set_auth(password)
    nation.gift_card(card_id, card_season, prize_winner)
    nation.rmb_post(region.region_name, f"Congratulations [nation]{prize_winner}[/nation], [b]you won the prize draw![/b]\nYou will receive card number [i]{card_id}[/i], from season {card_season}.")
    print("Done.")

grand_prize()