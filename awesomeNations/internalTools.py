from awesomeNations.customMethods import format_key, string_is_number, join_keys
from awesomeNations.exceptions import DataError
from pprint import pprint as pp
from typing import Optional, Literal
import xmltodict
import string
import random
import logging
from pathlib import Path
import urllib3

logger = logging.getLogger("AwesomeLogger")

class _ShardsQuery():
    def __init__(self,
                 api_family: tuple[str, str | None],
                 shards: Optional[str | list[str]] = None, 
                 params: Optional[dict[str, str | list[str]]] = None):
        if type(api_family) is not tuple:
            raise ValueError(f"api_family must be tuple, not '{type(api_family).__name__}'")
        
        self.api_family = api_family
        self.query_shards = shards
        self.query_params = params
        self._valid_shards = {
            "nation": ['admirable', 'admirables', 'animal', 'animaltrait', 'answered', 'banner*', 'banners*', 'capital', 'category', 'census**', 'crime', 'currency', 'customleader', 'customcapital', 'customreligion', 'dbid', 'deaths', 'demonym', 'demonym2', 'demonym2plural', 'dispatches', 'dispatchlist', 'endorsements', 'factbooks', 'factbooklist', 'firstlogin', 'flag', 'founded', 'foundedtime', 'freedom', 'fullname', 'gavote', 'gdp', 'govt', 'govtdesc', 'govtpriority', 'happenings', 'income', 'industrydesc', 'influence', 'influencenum', 'lastactivity', 'lastlogin', 'leader', 'legislation', 'majorindustry', 'motto', 'name', 'notable', 'notables', 'nstats', 'policies', 'poorest', 'population', 'publicsector', 'rcensus', 'region', 'religion', 'richest', 'scvote', 'sectors', 'sensibilities', 'tax', 'tgcanrecruit', 'tgcancampaign', 'type', 'wa', 'wabadges', 'wcensus', 'zombie'],
            "region": ['banlist', 'banner', 'bannerby', 'bannerurl', 'census', 'censusranks', 'dbid', 'delegate', 'delegateauth', 'delegatevotes', 'dispatches', 'embassies', 'embassyrmb', 'factbook', 'flag', 'founded', 'foundedtime', 'founder', 'frontier', 'gavote', 'governor', 'governortitle', 'happenings', 'history', 'lastupdate', 'lastmajorupdate', 'lastminorupdate', 'magnetism', 'messages', 'name', 'nations', 'numnations', 'wanations', 'numwanations', 'officers', 'poll', 'power', 'recruiters', 'scvote', 'tags', 'wabadges', 'zombie'],
            "world": ['banner', 'census', 'censusid', 'censusdesc', 'censusname', 'censusranks', 'censusscale', 'censustitle', 'dispatch', 'dispatchlist', 'faction', 'factions', 'featuredregion', 'happenings', 'lasteventid', 'nations', 'newnations', 'newnationdetails', 'numnations', 'numregions', 'poll', 'regions', 'regionsbytag', 'tgqueue'],
            "wa": ['numnations', 'numdelegates', 'delegates', 'members', 'happenings', 'proposals', 'resolution', 'voters', 'votetrack', 'dellog', 'delvotes', 'lastresolution']
        }
        
        self._validate_shards(self.query_shards) # Checks if shard(s) exists, if not, raises ValueError.

        if shards:
            if type(shards) is not str:
                self.query_shards = join_keys(shards)

        if params and type(params) is not str:
            for item in params:
                if type(params[item]) is not str:
                    params[item] = join_keys(params[item])
            self.query_params = join_keys([f"{p}={params[p]}" for p in params], ";")

    def querystring(self):
        querystring: str = "?"
        querystring += f"{self.api_family[0]}={self.api_family[1]}&" if self.api_family[0] != "world" else ""
        if self.query_shards:
            querystring += f"q={self.query_shards}"
        else:
            querystring = querystring.replace("&", "")
        if self.query_params:
            querystring += f";{self.query_params}"
        querystring += "&v={v}"
        return querystring

    def _validate_shards(self, shards: str | list[str]) -> None:
        valid = self._valid_shards[self.api_family[0]]
        if type(shards) == str:
            if not shards in valid:
                raise ValueError(f"Shard '{shards}' not found in {self.api_family[0].capitalize()} API family.")
        elif type(shards) == list or type(shards) == tuple:
            for shard in shards:
                print(shard)
                if not shard in valid:
                    raise ValueError(f"Shard '{shard}' not found in {self.api_family[0].capitalize()} API family.")
        else:
            raise ValueError(f"shards must be a str, list or tuple, not {type(shards).__name__}.")
                
class _DailyDataDumps():
    """
    Daily Data Dumps urls manager.
    """
    def __init__(self):
        self.nation_datadump = "https://www.nationstates.net/pages/nations.xml.gz"
        self.region_datadump = "https://www.nationstates.net/pages/regions.xml.gz"
    
    def get_dump(self, family: Literal["nation", "region"] = "nation"):
        match family:
            case "nation":
                return self.nation_datadump
            case "region":
                return self.region_datadump
            case _:
                raise ValueError(f"Sorry, I don't know '{family}' daily data dump. Maybe you misspelled it?")

    def dowload(self,
                   url: str,
                   filepath: str | Path) -> None:
        "Dowloads daily data dump."
        
        logger.debug(f"Dowloading Daily Data Dump: {url}")
        
        if not Path(filepath).suffix:
            raise ValueError(f"{filepath}: This path needs a suffix dude!")
        with urllib3.request("GET", url, preload_content=False) as file_response, open(filepath, "wb") as file_out:
            for chunk in file_response.stream(10**4, True):
                file_out.write(chunk)
        
        logger.debug(f"Daily Data Dump located in: {Path(filepath).absolute()}")

class _NationAuth():
    """Nation authentication"""
    def __init__(self,
                 password: Optional[str] = None,
                 autologin: Optional[str] = None):
        if not any((password, autologin)):
            raise ValueError("NationAuth can't be empty, a password or autologin must be given.")
        if password and type(password) is not str:
            raise ValueError(f"password must be str, not {type(password).__name__}")
        if autologin and type(autologin) is not str:
            raise ValueError(f"autologin must be str, not {type(autologin).__name__}")
        self.crip = _Criptografy()
        self.password = self.__secret__(password)
        self.autologin = self.__secret__(autologin)
        self.xpin: Optional[int] = None
    
    def __secret__(self, x: str):
        hidden_x = self.crip.encrypt(x) if x else ""
        return hidden_x

    def __show__(self, x: str):
        hidden_x = self.crip.decrypt(x) if x else ""
        return hidden_x
    
    def get(self) -> dict[str]:
        auth_headers: dict[str] = {
            "X-Password": self.__show__(self.password),
            "X-Autologin": self.__show__(self.autologin),
            "X-Pin": self.xpin if self.xpin else ""
        }
        return auth_headers

class _PrivateCommand():
    def __init__(self,
                 nation_name: str,
                 command: str, 
                 params: Optional[dict[str, str | list[str]]],
                 allow_beta: bool = False):        
        self.valid = ["issue", "giftcard", "dispatch", "rmbpost"]
        self.not_prepare = ["issue"] # Commands that don't need preparing.
        self.beta_commands = ["dispatch", "rmbpost", "giftcard"] # Commands still in beta (under development).
        
        if command in self.beta_commands and not allow_beta:
            raise ValueError(f"Command '{command}' is a beta resource, to disable this exception, set allow_beta to True")
        
        self.nation_name = nation_name
        self.command_query = command
        self.command_params = params
        
        if type(command) is not str:
            raise ValueError(f"command must be str, not '{type(command).__name__}'")
        if command not in self.valid:
            raise ValueError(f"Not found a private command called '{command}'.")
        if len(params) < 1:
            raise ValueError("Private commands need extra parameters.")

        if type(params) is not str:
            for item in params:
                if type(params[item]) is not str:
                    params[item] = join_keys(params[item])
            self.command_params = join_keys([f"{p}={params[p]}" for p in params], "&")

    def command(self,
                        mode: Literal["prepare", "execute"] = "prepare",
                        token: str = None):
        command_url = self._querystring() + f"&mode={mode}"
        command_url += f"&token={token}" if token else ""
        command_url += "&v={v}"
        return command_url

    def _querystring(self):
        querystring: str = "?"
        querystring += f"nation={self.nation_name}&c={self.command_query}"
        querystring += f"&{self.command_params}"
        return querystring

class _AwesomeParser():
    def __init__(self):
        pass
    
    def parse_xml(self, data: dict[str]):
        """
        Parses XML data into a dictionary.
        """
        try:
            parsed_xml: dict = xmltodict.parse(data["data"], data["encoding"], postprocessor=self.xml_postprocessor)
            return parsed_xml
        except Exception as e:
            raise DataError("XML Data", e)

    def xml_postprocessor(self, path, key: str, value: str):
        key = format_key(key, replace_empty="_", delete_not_alpha=True)
        try:
            formatted_key: str = key
            formatted_value: str = value

            if string_is_number(formatted_value):
                formatted_value: complex = complex(formatted_value).real
                formatted_value = int(formatted_value) if formatted_value.is_integer() else formatted_value
            return formatted_key, formatted_value
        except (ValueError, TypeError):
            return key, value

class _Criptografy():
    "Basic substitution criptography!"
    def __init__(self):
        self.chars = " " + string.punctuation + string.digits + string.ascii_letters
        self.chars = list(self.chars)
        self.key = self.chars.copy()
        random.shuffle(self.key)
     
     # Encrypt stuff :D
    def encrypt(self, message_to_encrypt: str) -> str:
        plain_text = message_to_encrypt
        cipher_text = ""
        for letter in plain_text:
            index = self.chars.index(letter)
            cipher_text += self.key[index]
        return cipher_text

    # Decrypt stuff :D
    def decrypt(self, message_to_decrypt: str) -> str:
        cipher_text = message_to_decrypt
        plain_text = ""
        for letter in cipher_text:
            index = self.key.index(letter)
            plain_text += self.chars[index]
        return plain_text
    
    def exhaust(self):
        self.key = self.chars.copy()
        random.shuffle(self.key)

if __name__ == "__main__":
    shard_query = _ShardsQuery(("world", None), ("censusranks**"))
    print(shard_query.querystring())