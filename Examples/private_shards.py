from awesomeNations import AwesomeNations, Authentication
from dotenv import load_dotenv
from pprint import pp
import os

# Get sensitive data from .env file
load_dotenv()
password = os.environ["MY_PASSWORD"]

awesomeAPI = AwesomeNations("My application/1.0.0") # Replace this User-Agent with useful info.
nation = awesomeAPI.Nation("your nation name here!", Authentication(password))

data = nation.get_shards(('notices', 'ping', 'unread'))
pp(data)