from awesomeNations.connection import _WrapperConnection, _NationAPI, _RegionAPI
from awesomeNations.customMethods import format_key, gen_params, generate_epoch_timestamp
from awesomeNations.internalTools import _DailyDataDumps, _Secret, _ShardsQuery
from awesomeNations.exceptions import HTTPError
from pprint import pprint as pp
from datetime import datetime
from typing import Optional, Literal, Any
from urllib3 import Timeout
from pathlib import Path
from logging import WARNING, DEBUG
import logging
from bs4 import BeautifulSoup

global_wrapper: Any = None

logger = logging.getLogger("AwesomeLogger")
logging.basicConfig(level=logging.WARNING, format="[%(asctime)s] %(levelname)s: %(message)s")

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
    > the User-Agent header with **relevant** data.

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

    ### allow_beta:
    
    > Defines if AwesomeNations should allow beta resources to be used by you or not.
    """

    def __init__(self,
                 user_agent: str,
                 request_timeout: int | tuple = (15, 10),
                 ratelimit_sleep: bool = True,
                 ratelimit_reset_time: int = 30,
                 api_version: int = 12,
                 log_level: Optional[int] = WARNING,
                 allow_beta: bool = False):
        global global_wrapper # REMOVE IN THE NEXT MAJOR VERSION.
        self.user_agent = user_agent
        self.request_timeout: int | tuple[int, int] = request_timeout
        self.ratelimit_sleep: bool = ratelimit_sleep
        self.ratelimit_reset_time: int = ratelimit_reset_time
        self.api_version: int = api_version
        self.log_level: Optional[int] = log_level
        self.allow_beta = allow_beta

        self._wrapper_headers: dict[str, str] = {
        "User-Agent": "",
        "Cache-Control": "no-cache",
        }
        
        if self.log_level is None:
            logger.disabled = True
        elif type(self.log_level) is int:
            logger.level = self.log_level
        else:
            raise ValueError(f"Invalid {type(self.log_level).__name__} '{self.log_level}', log_level must be an int (to change level) or None (to disable logging)")
        
        if isinstance(self.request_timeout, tuple):
            self.request_timeout = Timeout(connect=(self.request_timeout[0]), read=self.request_timeout[1]) # type: ignore
        
        self._wrapper_connection = _WrapperConnection()
        self._wrapper_connection.setup(
            request_timeout = self.request_timeout,
            ratelimit_sleep = self.ratelimit_sleep,
            ratelimit_reset_time = self.ratelimit_reset_time,
            api_version = self.api_version,
            allow_beta = self.allow_beta
        )
        
        global_wrapper = self._wrapper_connection
        
        self.set_user_agent(self.user_agent)

    def __repr__(self):
        return f"AwesomeNations(user_agent='{self.user_agent}', request_timeout={self.request_timeout}, ratelimit_sleep={self.ratelimit_sleep}, ratelimit_reset_time={self.ratelimit_reset_time}, api_version={self.api_version}, log_level={self.log_level}, allow_beta={self.allow_beta})"

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

    def get_daily_data_dumps(self,
                             filepath: str | Path = "./datadump.gz",
                             type: Literal["nation", "region"] = "nation") -> None:
        """
        Dowloads NationStates daily data dumps.
        
        ### type: str
        
        - "nation": Dowloads the nation data dump.
        - "region": Dowloads the region data dump.
        """
        dumps = _DailyDataDumps()
        return dumps.dowload(dumps.get_dump(type), filepath)

    def get_world_shards(self,
                         shards: str | tuple[str, ...] | list[str],
                         **kwargs: Any) -> dict[str, dict[str, Any]]:
        """
        Gets one or more shards from the World API.
        """
        if not shards:
            raise ValueError("No shards provided and World API doesn't have a standard API.")
        url = wrapper.base_url + _ShardsQuery(("world", None), shards, kwargs).querystring() # type: ignore
        response: dict = self._wrapper_connection.fetch_api_data(url)
        return response

    def get_world_assembly_shards(self,
                                  shards: str | tuple[str, ...] | list[str],
                                  **kwargs: Any) -> dict[str, dict[str, Any]]:
        """
        Gets one or more shards from the World Assembly API.
        """
        if not shards:
            raise ValueError("No shards provided and World Assembly API doesn't have a standard API.")
        council_id = kwargs["council_id"]
        kwargs.pop("council_id")
        url = self._wrapper_connection.base_url + _ShardsQuery(("wa", council_id), shards, kwargs).querystring()
        response: dict = self._wrapper_connection.fetch_api_data(url)
        return response

    def get_api_latest_version(self) -> int:
        """Gets NationStates API latest version"""
        url = "https://www.nationstates.net/cgi-bin/api.cgi?a=version"
        latest_version: int = int(self._wrapper_connection.fetch_raw_data(url))
        return latest_version

    def get_wrapper_status(self) -> dict[str, Any]:
        """
        Gets wrapper data, such the number of requests seen.
        """
        status: dict[str, Any] = {
            "status": {
                "ratelimit_requests_seen": getattr(self._wrapper_connection, "ratelimit_requests_seen"),
            }
        }
        return status

    def set_user_agent(self, user_agent: str) -> None:
        """
        Sets AwesomeNations `user_agent`.
        """
        if not isinstance(user_agent, str):
            raise ValueError(f"user_agent must be type string, not {type(user_agent).__name__}")
        user_agent = user_agent.strip()
        if len(user_agent.replace(" ", "")) < 7:
            raise ValueError(f"'{user_agent}' is too short for a user_agent.")
        #setattr(self, "user_agent", user_agent)
        self._wrapper_headers.update({"User-Agent": user_agent})
        self._wrapper_connection.headers.update(self._wrapper_headers)

    def nation(self,
               nation_name: str,
               password: Optional[str] = None,
               autologin: Optional[str] = None) -> _NationAPI:
        new_nation = _NationAPI(nation_name)
        new_nation._set_wrapper(self._wrapper_connection)
                
        nation_password: Optional[_Secret] = _Secret(password) if password else None
        nation_autologin: Optional[_Secret] = _Secret(password) if password else None

        if any((nation_password, nation_autologin)):
            new_nation.set_auth(nation_password.reveal() if nation_password else None,
                                nation_autologin.reveal() if nation_autologin else None)
        return new_nation

    def region(self,
               region_name: str) -> _RegionAPI:
        new_region = _RegionAPI(region_name)
        new_region._set_wrapper(self._wrapper_connection)

        return new_region

    class Nation(_NationAPI):
        """
        **WARNING**: Deprecated, use AwesomeNations `nation()` instead.
        """
        def __init__(self, nation_name: str, password: str | None = None, autologin: str | None = None) -> None:
            super().__init__(nation_name)
            
            self._set_wrapper(global_wrapper)

            if password:
                if not isinstance(password, str):
                    raise ValueError(f"password must be type str, not {type(password).__name__}.")
                self.password = _Secret(password)
            if autologin:
                if not isinstance(autologin, str):
                    raise ValueError(f"autologin must be type str, not {type(autologin).__name__}.")
                self.autologin = _Secret(autologin)

            nation_password: Optional[_Secret] = self.password if self.password else None
            nation_autologin: Optional[_Secret] = self.autologin if self.autologin else None
            
            if any((nation_password, nation_autologin)):
                self.set_auth(nation_password.reveal() if nation_password else None,
                            nation_autologin.reveal() if nation_autologin else None)
            
            logger.warning(f"{type(self).__name__} is deprecated, use AwesomeNations nation() instead.")

    class Region(_RegionAPI):
        """
        **WARNING**: Deprecated, use AwesomeNations `region()` instead.
        """
        def __init__(self, region_name: str) -> None:
            super().__init__(region_name)
            
            self._set_wrapper(global_wrapper)
            
            logger.warning(f"{type(self).__name__} is deprecated, use AwesomeNations region() instead.")

if __name__ == "__main__":
    api = AwesomeNations("AwesomeNations/Test", log_level=DEBUG)
    ...