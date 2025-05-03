from awesomeNations.customMethods import format_key, string_is_number, join_keys
from awesomeNations.exceptions import DataError
from pprint import pprint as pp
from typing import Optional, Literal
import xmltodict
import logging
from pathlib import Path
import urllib3
import json
from bs4 import BeautifulSoup
import re

logger = logging.getLogger("AwesomeLogger")

class _Secret():
    """
    Stores a string value and hides it from string representation.
    
    `value` is the value to be stored. If `single_use` is `True`, the value will be set to ``None`` after being revealed once.
    """
    def __init__(self, value: str, single_use: bool = False):
        if type(value) is _Secret:
            raise ValueError("You can't have a _Secret inside another _Secret.")
        self._value: Optional[str] = str(value) if value else None
        self.single_use: bool = single_use
    
    def __str__(self):
        return "<hidden>"
    
    def __repr__(self):
        return "<hidden>"
    
    def __getattribute__(self, name):
        if name in ('__str__', '__repr__'):
            return lambda: "<hidden>"
        if name == '_value':
           return "<hidden>"
        return object.__getattribute__(self, name)
    
    def __dir__(self):
        return [attr for attr in super().__dir__() if attr != '_value']

    def __bool__(self):
        return object.__getattribute__(self, "_value") is not None

    def __eq__(self, other: object) -> bool:
        if isinstance(other, _Secret):
            return object.__getattribute__(self, "_value") == object.__getattribute__(other, "_value")
        return object.__getattribute__(self, "_value") == other

    def reveal(self) -> Optional[str]:
        try:
            return object.__getattribute__(self, "_value")
        finally:
            if self.single_use:
                object.__setattr__(self, "_value", None)

class _ShardsQuery():
    def __init__(self,
                 api_family: tuple[Literal["nation", "region", "world", "wa"], str | None],
                 shards: Optional[str | list[str]] = None, 
                 params: Optional[dict[str, str | list[str]]] = None):
        if type(api_family) is not tuple:
            raise ValueError(f"api_family must be tuple, not '{type(api_family).__name__}'")
        
        self.api_family = api_family
        self.query_shards = shards
        self.query_params = params
        self._valid_shards = {
            "nation": ['admirable', 'admirables', 'animal', 'animaltrait', 'answered', 'banner*', 'banners*', 'capital', 'category', 'census**', 'crime', 'currency', 'customleader', 'customcapital', 'customreligion', 'dbid', 'deaths', 'demonym', 'demonym2', 'demonym2plural', 'dispatches', 'dispatchlist', 'endorsements', 'factbooks', 'factbooklist', 'firstlogin', 'flag', 'founded', 'foundedtime', 'freedom', 'fullname', 'gavote', 'gdp', 'govt', 'govtdesc', 'govtpriority', 'happenings', 'income', 'industrydesc', 'influence', 'influencenum', 'lastactivity', 'lastlogin', 'leader', 'legislation', 'majorindustry', 'motto', 'name', 'notable', 'notables', 'nstats', 'policies', 'poorest', 'population', 'publicsector', 'rcensus', 'region', 'religion', 'richest', 'scvote', 'sectors', 'sensibilities', 'tax', 'tgcanrecruit', 'tgcancampaign', 'type', 'wa', 'wabadges', 'wcensus', 'zombie', 'dossier', 'issues', 'issuesummary', 'nextissue', 'nextissuetime', 'notices', 'packs', 'ping', 'rdossier', 'unread'],
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
        return querystring

    def _validate_shards(self, shards: str | list[str]) -> None:
        valid = self._valid_shards[self.api_family[0]]
        if type(shards) == str:
            if not shards in valid:
                raise ValueError(f"Shard '{shards}' not found in {self.api_family[0].capitalize()} API family.")
        elif type(shards) == list or type(shards) == tuple:
            for shard in shards:
                if not shard in valid:
                    raise ValueError(f"Shard '{shard}' not found in {self.api_family[0].capitalize()} API family.")
        else:
            if shards:
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
        
        filepath = Path(filepath)
        
        if not filepath.suffix:
            filepath = filepath.with_suffix(".gz")
        if filepath.suffix != ".gz":
            raise ValueError(f"{filepath.as_posix()}: '{filepath.suffix}' is not a valid suffix.")
        with urllib3.request("GET", url, preload_content=False) as file_response, open(filepath, "wb") as file_out:
            for chunk in file_response.stream(10**4, True):
                file_out.write(chunk)
        
        logger.info(f"Daily data dump located in: {Path(filepath).absolute()}")

class _NationAuth():
    """Nation authentication"""
    def __init__(self,
                 password: Optional[_Secret] = None,
                 autologin: Optional[_Secret] = None):
        if password and type(password) is not _Secret:
            raise ValueError(f"password must be _Secret, not {type(password).__name__}.")
        if autologin and type(autologin) is not _Secret:
            raise ValueError(f"autologin must be _Secret, not {type(autologin).__name__}.")
        self.password = password
        self.autologin = autologin
        self.xpin: Optional[_Secret] = None
    
    def get(self) -> dict[str]:
        auth_headers: dict[str] = {
            "X-Password": self.password.reveal() if self.password.reveal() else "",
            "X-Autologin": self.autologin.reveal() if self.autologin.reveal() else "",
            "X-Pin": self.xpin.reveal() if self.xpin else ""
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
    
    def parse_xml(self, content: bytes | str, encoding: str):
        """
        Parses XML data into a dictionary.
        """
        try:
            parsed_xml: dict = xmltodict.parse(content, encoding, postprocessor=self.xml_postprocessor)
            return json.loads(json.dumps(parsed_xml))
        except Exception as e:
            raise DataError("XML Data", e)

    def parse_html_in_string(self, string: str):
        try:
            soup = BeautifulSoup(string, 'html.parser')
            tags = [tag for tag in soup.find_all()]

            if "<br>" in string:
                string = string.replace("<br>", "\n")
            for tag in tags:
                #print(tag.attrs["href"])
                string = string.replace(str(tag), str(tag.text if not tag.name == "a" else f"{tag.text}: '{tag.attrs["href"]}'"))
            # Remove remenants of undetected HTML tags
            string = re.sub(r"<[^>]+>", "", string)
            return string
        except:
            return string

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

if __name__ == "__main__":
    parser = _AwesomeParser()
    html_data = """New factbook posted! <a href="/nation=orlys/detail=factbook/id=2650467">View Your Factbook</a>"""
    parsed_data = parser.parse_html_in_string(html_data)
    print(parsed_data)