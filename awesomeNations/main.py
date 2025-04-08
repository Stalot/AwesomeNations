from awesomeNations.connection import _WrapperConnection
from awesomeNations.customMethods import join_keys, format_key, generate_epoch_timestamp
from awesomeNations.internalTools import _NationAuth, _ShardsQuery, _DailyDataDumps, _PrivateCommand
from awesomeNations.exceptions import HTTPError
from pprint import pprint as pp
from datetime import datetime
from typing import Optional
from urllib3 import Timeout
from typing import Literal
from pathlib import Path
from logging import WARNING, DEBUG
import logging

logger = logging.getLogger("AwesomeLogger")
logging.basicConfig(level=logging.WARNING, format="[%(asctime)s] %(levelname)s: %(message)s")

wrapper = _WrapperConnection()

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
                 log_level: Optional[int] = WARNING):
        self.user_agent: str = user_agent
        self.request_timeout: int | tuple = request_timeout
        self.ratelimit_sleep: bool = ratelimit_sleep
        self.ratelimit_reset_time: int = ratelimit_reset_time
        self.api_version: int = api_version
        self.log_level: Optional[int] = log_level

        headers: dict = {
        "User-Agent": self.user_agent,
        "Cache-Control": "no-cache",
        }
        
        wrapper.headers = headers
        wrapper.request_timeout = Timeout(connect=self.request_timeout[0], read=self.request_timeout[1]) if type(self.request_timeout) is tuple else int(self.request_timeout)
        wrapper.ratelimit_sleep = self.ratelimit_sleep
        wrapper.ratelimit_reset_time = self.ratelimit_reset_time
        wrapper.api_version = self.api_version
        
        if self.log_level is None:
            logger.disabled = True
        elif type(self.log_level) is int:
            logger.level = self.log_level
        else:
            raise ValueError(f"Invalid {type(self.log_level).__name__} '{self.log_level}', log_level must be an int (to change level) or None (to disable logging)")

    def __repr__(self):
        return f"AwesomeNations(user_agent={self.user_agent}, request_timeout={self.request_timeout}, ratelimit_sleep={self.ratelimit_sleep}, ratelimit_reset_time={self.ratelimit_reset_time}, api_version={self.api_version}, log_level={self.log_level})"

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
            wrapper._auth = _NationAuth(password, autologin) if any((password, autologin)) else None

        def __repr__(self):
            return f"Nation(nation_name={self.nation_name})"

        def exists(self) -> bool:
            """
            Checks if nation exists.
            """
            url = wrapper.base_url + _ShardsQuery(("nation", self.nation_name)).querystring()
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

        def execute_command(self, c: str, **kwargs) -> None:
            """
            # BETA
            Executes private commands.
            """
            if len(kwargs) < 1:
                raise ValueError("Private commands need extra parameters.")
            command = _PrivateCommand(self.nation_name,
                                      c,
                                      kwargs)
            logger.info(f"Preparing private command: {c}...")
            
            prepare_response: dict = wrapper.fetch_api_data(wrapper.base_url + command.command("prepare"))
            prepare_status: bool = True if prepare_response["nation"].get("success") else False
            if prepare_status:
                token: str | None = prepare_response.get("nation").get("success")
                
                logger.info(f"Executing private command: {c}...")
                
                execute_response: dict = wrapper.fetch_api_data(wrapper.base_url + command.command("execute", token))
                execute_status: bool = True if execute_response["nation"].get("success") else False
                if not execute_status:
                    raise ValueError(f"Could not execute private command: {execute_response["nation"]["error"]}")
                logger.info(f"Private command complete: {execute_response["nation"]["success"]}")
                return None
            raise ValueError(f"Could not prepare private command for execution: {prepare_response["nation"]["error"]}")

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