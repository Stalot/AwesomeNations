from awesomeNations.customMethods import format_key, string_is_number, gen_params
from awesomeNations.exceptions import DataError
from pprint import pprint as pp
from typing import Optional, Literal, Any, Iterable, Iterator
import xmltodict
import logging
from pathlib import Path
import urllib3
import json
from bs4 import BeautifulSoup
import re

logger = logging.getLogger("AwesomeLogger")

class _ItemSequence(Iterator):
    """
    _ItemSequence is an iterator class that wraps a sequence of items,
    allowing iteration over them one by one.
    
    **Note**: If an iterator or generator is passed, it will be consumed
    and stored as a list internally.

    ***

    Parameters:
        items (Any): The items to be wrapped. Can be a single item,
                    a list, tuple, iterator, or any iterable.
    """
    def __init__(self, items: Any) -> None:
        if not isinstance(items, (list, tuple, Iterator)):
            self._items: list[Any] = [items]
        else:
            self._items: list[Any] = [item for item in items]
        
        self._current_index: int = -1
    
    def __iter__(self) -> Iterator:
        return self
    
    def __next__(self) -> Any:
        self._current_index += 1
        if not self._current_index >= (len(self._items)):
            return self._items[self._current_index]
        raise StopIteration
    
    def __len__(self):
        return len(self._items)
    
    def __getitem__(self, index: int) -> Any:
        if not index <= len(self._items):
            raise IndexError(f"Index {index} is out of range. Valid range for this {type(self).__name__} instance is 0 to {len(self._items) - 1}.")
        return self._items[index]

    def __str__(self):
        return f"{type(self).__name__}(*{len(self._items)} items*...)"

    def __repr__(self):
        return f"{type(self).__name__}(items={self._items})"

    def get_items(self) -> Any:
        return self._items

    def join_items(self,
                   separator: str):
        """
        Joins all items in a single string.
        """
        return separator.join([str(item) for item in self._items])

    def copy(self):
        return _ItemSequence(self._items)

class _Secret():
    """
    Stores a string value and hides it from string representation.
    
    `value` is the value to be stored. If `single_use` is `True`, the value will be set to ``None`` after being revealed once.
    """
    def __init__(self, value: Any, single_use: bool = False):
        if isinstance(value, _Secret):
            raise ValueError("You can't have a _Secret inside another _Secret.")
        self._value: Any = value
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

    def reveal(self) -> Optional[Any]:
        try:
            return object.__getattribute__(self, "_value")
        finally:
            if self.single_use:
                object.__setattr__(self, "_value", None)

class _ShardsQuery():
    def __init__(self,
                 api_family: tuple[Literal["nation", "region", "world", "wa"], Optional[str]],
                 shards: Optional[Iterable[str]] = None, 
                 params: Optional[dict[str, Any]] = None):
        if type(api_family) is not tuple:
            raise ValueError(f"api_family must be tuple, not '{type(api_family).__name__}'")
        
        self._api_family: tuple[str, Optional[str]] = api_family
        self._shards: Optional[_ItemSequence | str] = _ItemSequence(shards)
        self._params: Optional[dict[str, Any]] = params
        self._valid_shards: dict[str, list[str]] = {
            "nation": ['admirable', 'admirables', 'animal', 'animaltrait', 'answered', 'banner', 'banners', 'capital', 'category', 'census', 'crime', 'currency', 'customleader', 'customcapital', 'customreligion', 'dbid', 'deaths', 'demonym', 'demonym2', 'demonym2plural', 'dispatches', 'dispatchlist', 'endorsements', 'factbooks', 'factbooklist', 'firstlogin', 'flag', 'founded', 'foundedtime', 'freedom', 'fullname', 'gavote', 'gdp', 'govt', 'govtdesc', 'govtpriority', 'happenings', 'income', 'industrydesc', 'influence', 'influencenum', 'lastactivity', 'lastlogin', 'leader', 'legislation', 'majorindustry', 'motto', 'name', 'notable', 'notables', 'nstats', 'policies', 'poorest', 'population', 'publicsector', 'rcensus', 'region', 'religion', 'richest', 'scvote', 'sectors', 'sensibilities', 'tax', 'tgcanrecruit', 'tgcancampaign', 'type', 'wa', 'wabadges', 'wcensus', 'zombie', 'dossier', 'issues', 'issuesummary', 'nextissue', 'nextissuetime', 'notices', 'packs', 'ping', 'rdossier', 'unread'],
            "region": ['banlist', 'banner', 'bannerby', 'bannerurl', 'census', 'censusranks', 'dbid', 'delegate', 'delegateauth', 'delegatevotes', 'dispatches', 'embassies', 'embassyrmb', 'factbook', 'flag', 'founded', 'foundedtime', 'founder', 'frontier', 'gavote', 'governor', 'governortitle', 'happenings', 'history', 'lastupdate', 'lastmajorupdate', 'lastminorupdate', 'magnetism', 'messages', 'name', 'nations', 'numnations', 'wanations', 'numwanations', 'officers', 'poll', 'power', 'recruiters', 'scvote', 'tags', 'wabadges', 'zombie'],
            "world": ['banner', 'census', 'censusid', 'censusdesc', 'censusname', 'censusranks', 'censusscale', 'censustitle', 'dispatch', 'dispatchlist', 'faction', 'factions', 'featuredregion', 'happenings', 'lasteventid', 'nations', 'newnations', 'newnationdetails', 'numnations', 'numregions', 'poll', 'regions', 'regionsbytag', 'tgqueue'],
            "wa": ['numnations', 'numdelegates', 'delegates', 'members', 'happenings', 'proposals', 'resolution', 'voters', 'votetrack', 'dellog', 'delvotes', 'lastresolution']
        }
                
        self._validate_shards(self._shards) # Checks if shard(s) exists, if not, raises ValueError.

        self._query_shards: Optional[str] = None
        self._query_params: Optional[str] = None
        
        if self._shards:
            self._query_shards = self._shards.join_items("+")
        if self._params:
            self._query_params = gen_params(self._params, True) # type: ignore

    def querystring(self):
        querystring: str = "?"
        querystring += f"{self._api_family[0]}={self._api_family[1]}&" if self._api_family[0] != "world" else ""
        if self._shards:
            querystring += f"q={self._query_shards}"
        else:
            querystring = querystring.replace("&", "")
        if self._params:
            querystring += f";{self._query_params}"
        return querystring

    def _validate_shards(self, shards: Optional[_ItemSequence]) -> None:
        valid = self._valid_shards[self._api_family[0]]
        if shards:
            for shard in shards:
                if not shard in valid:
                    raise ValueError(f"Shard '{shard}' not found in {self._api_family[0].capitalize()} API family.")
                
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

    def __repr__(self):
        return f"_NationAuth({self.password}, {self.autologin})"
    
    def get(self) -> dict[str, str]:
        """
        **WARNING**: This method **reveals** sensitive info, don't print it!
        
        ***
        
        Gets _NationAuth data.
        """
        auth_headers: dict[str, Any] = {
            "X-Password": self.password,
            "X-Autologin": self.autologin,
            "X-Pin": self.xpin
        }
        auth_headers = {k: v.reveal() for k, v in auth_headers.items() if v != None and isinstance(v, _Secret)}
        return auth_headers

class _AuthManager():
    """
    Manage authentications.
    """
    def __init__(self):
        self.authentications: dict[str, _NationAuth] = {}

    def update_auth(self,
                    id: Optional[str],
                    password: Optional[_Secret] = None,
                    autologin: Optional[_Secret] = None,
                    xpin: Optional[_Secret] = None):
        if id:
            if self.authentications.get(id):
                if self.authentications[id].password != password and password:
                    self.authentications[id].password = password
                if self.authentications[id].autologin != autologin and autologin:
                    self.authentications[id].autologin = autologin
                if self.authentications[id].xpin != xpin and xpin:
                    self.authentications[id].xpin = xpin
            else:
                new_auth = _NationAuth(password, autologin)
                new_auth.xpin = xpin
                self.authentications.update({id: new_auth})
    
    def get_all(self):
        return self.authentications

    def get(self, id):
        return self.authentications[id]
    
    def forget(self, id):
        self.authentications.pop(id)

class _PrivateCommand():
    def __init__(self,
                 nation_name: Optional[str],
                 command: str,
                 params: dict[str, Any] | str,
                 allow_beta: bool = False):        
        self.valid = ["issue", "giftcard", "dispatch", "rmbpost"]
        self.not_prepare = ["issue"] # Commands that don't need preparing.
        self.beta_commands = ["dispatch", "rmbpost", "giftcard"] # Commands still in beta (under development).
        
        if command in self.beta_commands and not allow_beta:
            raise ValueError(f"Command '{command}' is a beta resource, to disable this exception, set allow_beta to True")
        
        self.nation_name = nation_name
        self.command_query = command
        self.command_params = params
        
        if not isinstance(command, str):
            raise ValueError(f"command must be str, not '{type(command).__name__}'")
        if command not in self.valid:
            raise ValueError(f"Not found a private command called '{command}'.")
        if isinstance(params, dict) and len(params.keys()) < 1:
            raise ValueError("Private commands need extra parameters.")

    def command(self,
                        mode: Literal["prepare", "execute"] = "prepare",
                        token: Optional[str] = None):
        command_url = self._querystring() + f"&mode={mode}"
        command_url += f"&token={token}" if token else ""
        command_url += "&v={v}"
        return command_url

    def _querystring(self):
        querystring: str = "?"
        querystring += f"nation={self.nation_name}&c={self.command_query}"
        querystring += f"&{gen_params(self.command_params, join=True)}"
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
            raise DataError("XML Data", str(e))

    def parse_html_in_string(self, string: str):
        try:
            soup = BeautifulSoup(string, 'html.parser')
            tags = [tag for tag in soup.find_all()]

            if "<br>" in string:
                string = string.replace("<br>", "\n")
            for tag in tags:
                #print(tag.attrs["href"])
                string = string.replace(str(tag), str(tag.text if not tag.name == "a" else f"{tag.text}: '{tag.attrs["href"]}'")) # type: ignore
            # Remove remenants of undetected HTML tags
            string = re.sub(r"<[^>]+>", "", string)
            return string
        except:
            return string

    def xml_postprocessor(self, path, key: str, value: str):
        key = format_key(key, replace_empty="_", delete_not_alpha=True)
        try:
            if string_is_number(value):
                formatted_value: complex = complex(value).real
                formatted_value = int(formatted_value) if formatted_value.is_integer() else formatted_value
            return key, value
        except (ValueError, TypeError):
            return key, value

if __name__ == "__main__":
    authManager = _AuthManager()
    
    authManager.update_auth("orlys", password=_Secret("12345"), xpin=_Secret("343535323"))
    authManager.update_auth("orlys", password=_Secret("1234523423"), xpin=None)
    authManager.update_auth("dives_patriae", password=_Secret("12345"), xpin=_Secret("343535324"))
    authManager.update_auth("fullworthia", password=_Secret("12345"), xpin=_Secret("343535325"))
    authManager.update_auth("ponytus", password=_Secret("12345"), xpin=_Secret("343535326"))
    
    authManager.forget("ponytus")
    
    pp(authManager.get_all())