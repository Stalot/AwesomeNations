from awesomeNations.connection import _WrapperConnection
from awesomeNations.customMethods import join_keys, format_key, generate_epoch_timestamp
from awesomeNations.internalTools import _NationAuth, _ShardsQuery, _DailyDataDumps, _PrivateCommand, _Secret, _AwesomeParser
from awesomeNations.exceptions import HTTPError
from pprint import pprint as pp
from datetime import datetime
from typing import Optional
from urllib3 import Timeout
from typing import Literal, Any
from pathlib import Path
from logging import WARNING, DEBUG
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger("AwesomeLogger")
logging.basicConfig(level=logging.WARNING, format="[%(asctime)s] %(levelname)s: %(message)s")

wrapper = _WrapperConnection()
parser = _AwesomeParser()

class AwesomeNations():
    """
    # 🚩 AwesomeNations 🚩

    Welcome! I'm the main class of this library and can't wait to collaborate with you!
    Feel free to explore my [GitHub repository](https://github.com/Stalot/AwesomeNations)
    and report any issues [here](https://github.com/Stalot/AwesomeNations/issues).

    # 📚 Useful References 📚
    
    If you want to make things right, I highly recommend you to **read documentation**.
    Yes, I know, it sounds as thrilling as watching paint dry... But you really should!
    Here are some helpful links for coding guidelines and references. Please note that
    these resources may change over time:

    - 📖 [NationStates API Documentation](https://www.nationstates.net/pages/api.html)  
    - ⚖️ [NationStates Script Rules for HTML site](https://forum.nationstates.net/viewtopic.php?p=16394966#p16394966)
    
    ---
    
    ### user_agent:

    > Sets a User-Agent. Whenever possible, your tool should identify itself by setting
    > the User-Agent header with relevant data.

    > - `<application name>/<version> <comments>`
    > - `ExampleScript/1.2 (by:Testlandia; usedBy:Maxtopia)`
    
    ### request_timeout:

    > Defines a timeout (in seconds) for requests.

    > - `request_timeout: tuple = (10, 5)` -> 10 seconds for connecting, 5 seconds for reading.
    > - `request_timeout: int = 10` -> 10 seconds for both.
    
    ### ratelimit_sleep:
    
    > This allows to automatically "sleep" if the API ratelimit is reached, prevents temporary
    > lockouts due to excessive requests in a short span of time.

    ### ratelimit_reset_time:
    
    > Defines the reset time (in seconds) to wait when the API ratelimit is reached.
    
    ### api_version:
    
    > This setting allows you to specify the NationStates API version your script uses.

    ### log_level:
    
    > Sets logging log level, if None is given, disables logging.
    """

    def __init__(self,
                 user_agent: str,
                 request_timeout: int | tuple = (15, 10),
                 ratelimit_sleep: bool = True,
                 ratelimit_reset_time: int = 30,
                 api_version: int = 12,
                 log_level: Optional[int] = WARNING,
                 allow_beta: bool = False):
        self.user_agent: str = user_agent
        self.request_timeout: int | tuple = request_timeout
        self.ratelimit_sleep: bool = ratelimit_sleep
        self.ratelimit_reset_time: int = ratelimit_reset_time
        self.api_version: int = api_version
        self.log_level: Optional[int] = log_level
        self.allow_beta = allow_beta

        headers: dict = {
        "User-Agent": self.user_agent,
        "Cache-Control": "no-cache",
        }
        
        wrapper.setup(
            headers=headers,
            request_timeout = Timeout(connect=self.request_timeout[0], read=self.request_timeout[1]) if type(self.request_timeout) is tuple else int(self.request_timeout),
            ratelimit_sleep = self.ratelimit_sleep,
            ratelimit_reset_time = self.ratelimit_reset_time,
            api_version = self.api_version,
            allow_beta = self.allow_beta
        )
        
        if self.log_level is None:
            logger.disabled = True
        elif type(self.log_level) is int:
            logger.level = self.log_level
        else:
            raise ValueError(f"Invalid {type(self.log_level).__name__} '{self.log_level}', log_level must be an int (to change level) or None (to disable logging)")

    def __repr__(self):
        return f"AwesomeNations(user_agent={self.user_agent}, request_timeout={self.request_timeout}, ratelimit_sleep={self.ratelimit_sleep}, ratelimit_reset_time={self.ratelimit_reset_time}, api_version={self.api_version}, log_level={self.log_level}, allow_beta={self.allow_beta})"

    def today_is_nationstates_birthday(self) -> bool:
        "Today is 11/13?"
        today = datetime.today()
        date: str = today.strftime('%D')
        birthday: bool = False
        if '11/13' in date:
            birthday = True
        return birthday

    def get_nationstates_age(self) -> int:
        "Current year - NationStates year of creation (NationStates was created in 2002)."
        created = 2002
        today = datetime.today().year
        age = today - created
        return age

    def get_daily_data_dumps(self, filepath: str | Path = "./datadump.gz", type: Literal["nation", "region"] = "nation") -> None:
        """
        Dowloads NationStates daily data dumps.
        
        ### type: str
        
        - "nation": Dowloads the nation data dump.
        - "region": Dowloads the region data dump.
        """
        dumps = _DailyDataDumps()
        return dumps.dowload(dumps.get_dump(type), filepath)

    def get_world_shards(self, shards: str | tuple[str] | list[str], **kwargs) -> dict:
        """
        Gets one or more shards from the World API.
        """
        if not shards:
            raise ValueError("No shards provided and World API doesn't have a standard API.")
        url = wrapper.base_url + _ShardsQuery(("world", None), shards, kwargs).querystring()
        response: dict = wrapper.fetch_api_data(url)
        return response

    def get_world_assembly_shards(self, shards: str | tuple[str] | list[str], **kwargs) -> dict:
        """
        Gets one or more shards from the World Assembly API.
        """
        if not shards:
            raise ValueError("No shards provided and World Assembly API doesn't have a standard API.")
        council_id = kwargs["council_id"]
        kwargs.pop("council_id")
        url = wrapper.base_url + _ShardsQuery(("wa", council_id), shards, kwargs).querystring()
        print(url)
        response: dict = wrapper.fetch_api_data(url)
        return response

    def get_api_latest_version(self) -> int:
        """Gets NationStates API latest version"""
        url = "https://www.nationstates.net/cgi-bin/api.cgi?a=version"
        latest_version: int = int(wrapper.fetch_raw_data(url))
        return latest_version

    class Nation:
        """
        Class dedicated to NationStates nation API.
        """
        def __init__(self,
                     nation_name: str,
                     password: str = None,
                     autologin: str = None) -> None:
            self.nation_name: str = format_key(nation_name, False, '%20') # Name is automatically parsed.
            self.password: Optional[_Secret] = _Secret(password)
            self.autologin: Optional[_Secret] = _Secret(autologin)
            
            if any((password, autologin)):
                self.set_auth(self.password.reveal(), self.autologin.reveal())
            # wrapper._auth = _NationAuth(self.authentication[0], self.authentication[1]) if any((password, autologin)) else None

        def __repr__(self):
            return f"Nation(nation_name={self.nation_name})"
    
        def set_auth(self, password: str = None, autologin: str = None):
            if any((password, autologin)):
                self.password = _Secret(password)
                self.autologin = _Secret(autologin)
                new_auth = _NationAuth(self.password, self.autologin)
                setattr(wrapper, '_auth', new_auth)
            else:
                raise ValueError("At least a password or an autologin must be given.")
    
        def exists(self) -> bool:
            """
            Checks if nation exists.
            """
            url = wrapper.base_url + f"?nation={self.nation_name}"
            status_code: int = wrapper.connection_status_code(url)
            match status_code:
                case 200:
                    return True
                case 404:
                    return False
                case _:
                    raise HTTPError(status_code)

        # DEPRECATED METHOD
        def get_public_shards(self, shards: Optional[str | tuple[str] | list[str]] = None, **kwargs) -> dict:
            """
            # THIS METHOD IS DEPRECATED
            ## Use ```get_shards()``` instead!
            
            ***
            
            Gets one or more shards from the requested nation, returns the standard API if no shards provided.
            
            ### Standard:
            
            > A compendium of the most commonly sought information.
            
            ### Shards:
            > If you don't need most of this data, please use shards instead. Shards allow you to request
            > exactly what you want and can be used to request data not available from the Standard API!
            """
            url = wrapper.base_url + _ShardsQuery(("nation", self.nation_name), shards, kwargs).querystring()
            logger.warning("get_public_shards() is deprecated.")
            response: dict = wrapper.fetch_api_data(url)
            return response

        # Replacing get_public_shards()
        def get_shards(self, shards: Optional[str | tuple[str] | list[str]] = None, **kwargs) -> dict:
            """
            Gets one or more shards from the requested nation, returns the standard API if no shards provided.
            
            ### Standard:
            
            > A compendium of the most commonly sought information.
            
            ### Shards:
            > If you don't need most of this data, please use shards instead. Shards allow you to request
            > exactly what you want and can be used to request data not available from the Standard API!
            """
            url = wrapper.base_url + _ShardsQuery(("nation", self.nation_name), shards, kwargs).querystring()
            response: dict = wrapper.fetch_api_data(url)
            return response

        def execute_command(self, c: Literal["issue", "giftcard", "dispatch", "rmbpost"], **kwargs) -> dict[str, Any]:
            """
            Executes private commands.
            """
            command = _PrivateCommand(self.nation_name,
                                      c,
                                      kwargs,
                                      wrapper.allow_beta)
            token: str | None = None
            if not c in command.not_prepare:
                logger.info(f"Preparing private command: '{c}'...") 
                prepare_response: dict = wrapper.fetch_api_data(wrapper.base_url + command.command("prepare"))
                token = prepare_response.get("nation").get("success")
                if not token:
                    return prepare_response
    
            logger.info(f"Executing private command: '{c}'...")
            execute_response: dict = wrapper.fetch_api_data(wrapper.base_url + command.command("execute", token))
            return execute_response

        def dispatch(self,
                     action: Literal["add", "edit", "remove"],
                     id: Optional[int] = None,
                     title: Optional[str] = None,
                     text: Optional[str] = None,
                     category: Optional[int] = None,
                     subcategory: Optional[int] = None) -> dict[str, dict]:
            """
            # BETA:
            Currently in development. Subject to change without warning.
            
            ---
            
            Creates, edits and deletes dispatches.
            """
            if not action == "add" and not id:
                raise ValueError(f"action '{action}' needs a valid dispatch id!")
            if (action == "add" or action == "edit") and not all((title, text, category, subcategory)):
                raise ValueError(f"action '{action}' needs a valid title, text, category and subcategory.")

            if category and not type(category) == int:
                raise ValueError(f"category must be int, not type '{type(category).__name__}'.")
            if subcategory and not type(subcategory) == int:
                raise ValueError(f"subcategory must be int, not type '{type(subcategory).__name__}'.")
            
            query_params = {
                "dispatchid": id,
                "dispatch": action,
                "title": title.replace(" ", "%20") if title else title,
                "text": text.replace(" ", "%20") if text else text,
                "category": category,
                "subcategory": subcategory
            }
            for key, value in list(query_params.items()):
                if not value:
                    query_params.pop(key)
            
            c = _PrivateCommand(self.nation_name, "dispatch", query_params, wrapper.allow_beta)

            prepare_response: dict = wrapper.fetch_api_data(wrapper.base_url + c.command("prepare"))
            token = prepare_response.get("nation").get("success")
            
            if not token:
                raise ValueError(parser.parse_html_in_string(prepare_response["nation"]["error"]))
            
            execute_response: dict = wrapper.fetch_api_data(wrapper.base_url + c.command("execute", token))
            
            if execute_response["nation"].get("error"):
                raise ValueError(parser.parse_html_in_string(execute_response["nation"]["error"]))
            
            #soup = BeautifulSoup(execute_response["nation"]["success"], "html.parser")
            return execute_response

        def rmbpost(self,
                     region: str,
                     text: str) -> dict[str, dict]:
            """
            # BETA:
            Currently in development. Subject to change without warning.
            
            ---
            
            Post to a regional RMB.
            """                        
            query_params = {
                "nation": self.nation_name,
                "region": format_key(region, replace_empty="%20"),
                "text": text.replace(" ", "%20") if text else text,
            }
            
            c = _PrivateCommand(self.nation_name, "rmbpost", query_params, wrapper.allow_beta)

            prepare_response: dict = wrapper.fetch_api_data(wrapper.base_url + c.command("prepare"))
            token = prepare_response.get("nation").get("success")
            
            if not token:
                raise ValueError(parser.parse_html_in_string(prepare_response["nation"]["error"]))
            
            execute_response: dict = wrapper.fetch_api_data(wrapper.base_url + c.command("execute", token))
            
            if execute_response["nation"].get("error"):
                raise ValueError(parser.parse_html_in_string(execute_response["nation"]["error"]))
            
            #soup = BeautifulSoup(execute_response["nation"]["success"], "html.parser")
            return execute_response

    class Region: 
        """
        Class dedicated to NationStates region API.
        """
        def __init__(self, region_name: str) -> None:
            # self.pretty_name: str = prettify_string(str(region_name))
            self.region_name = format_key(region_name, False, '%20')
        
        def __repr__(self):
            return f"Region(region_name={self.region_name})"
        
        def exists(self) -> bool:
            """
            Checks if region exists.
            """
            url = wrapper.base_url + _ShardsQuery(("region", self.region_name)).querystring()
            status_code: int = wrapper.connection_status_code(url)
            match status_code:
                case 200:
                    return True
                case 404:
                    return False
                case _:
                    raise HTTPError(status_code)

        def get_shards(self, shards: Optional[str | tuple[str] | list[str]] = None, **kwargs) -> dict:
            """
            Gets one or more shards from the requested region, returns the standard API if no shards provided.
            
            ### Standard:
            
            A compendium of the most commonly sought information.
            
            ### Shards:
            If you don't need most of this data, please use shards instead. Shards allow you to request exactly what you want and can be used to request data not available from the Standard API!
            """
            url = wrapper.base_url + _ShardsQuery(("region", self.region_name), shards, kwargs).querystring()
            response: dict = wrapper.fetch_api_data(url)
            return response

if __name__ == "__main__":
    api = AwesomeNations("AwesomeNations/Test", log_level=DEBUG)
    nation = api.Nation("Orlys")