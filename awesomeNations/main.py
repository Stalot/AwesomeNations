from awesomeNations.connection import WrapperConnection, URLManager
from awesomeNations.customMethods import join_keys, format_key
from datetime import datetime
from bs4 import BeautifulSoup as bs
from pathlib import Path
from awesomeNations.exceptions import HTTPError
from pprint import pprint as pp

wrapper = WrapperConnection()
url_manager = URLManager("https://www.nationstates.net/cgi-bin/api.cgi")

class AwesomeNations():
    """
    # AwesomeNations

    Welcome! I'm the main class of this library and can't wait to collaborate with you! Feel free to explore my [GitHub repository](https://github.com/Stalot/AwesomeNations) and report any issues [here](https://github.com/Stalot/AwesomeNations/issues).

    ---

    ## 📚 Useful References

    Here are some helpful links for coding guidelines and references. Please note that these resources may change over time:

    - 📖 [NationStates API Documentation](https://www.nationstates.net/pages/api.html)  
    - ⚖️ [NationStates Script Rules for HTML site](https://forum.nationstates.net/viewtopic.php?p=16394966#p16394966)
    
    ---
    
    ## ⚙️ Class Arguments
    
    ### user_agent: str
    
    Sets a User-Agent. Whenever possible, your tool should identify itself by setting the User-Agent header with relevant data.
    - `<application name>/<version> <comments>`
    - `ExampleScript/1.2 (by:Testlandia; usedBy:Maxtopia)`
    
    ### session: bool
    
    Allow requesting using session, improving efficiency by maintaining persistent connections.
    
    ### request_timeout: int | tuple

    Defines a timeout (in seconds) for requests.

    - `request_timeout: tuple = (10, 5)` -> 10 seconds for connecting, 5 seconds for reading.
    - `request_timeout: int = 10` -> 10 seconds for both.
    
    ### ratelimit_sleep: bool
    
    This allows to automatically "sleep" if the API ratelimit is reached, prevents temporary lockouts due to excessive requests in a short span of time.

    ### ratelimit_reset_time: int
    
    Defines the reset time (in seconds) to wait when the API ratelimit is reached.
    
    ### api_version: int
    
    This setting allows you to specify the NationStates API version your script expects. Since the API may update over time, adding new data or changing its format, older scripts might break if they encounter unexpected changes. By requesting a specific version number, your script can ensure it receives data in a format it understands, preventing compatibility issues.
    """

    def __init__(self,
                 user_agent: str = None,
                 session: bool = False,
                 request_timeout: int = 15,
                 ratelimit_sleep: bool = True,
                 ratelimit_reset_time: int = 30,
                 api_version: int = 12):

        headers = {
        "User-Agent": user_agent,
        "Cache-Control": "no-cache",
        }
        
        wrapper.headers = headers
        wrapper.session = session
        wrapper.request_timeout = request_timeout
        wrapper.ratelimit_sleep = ratelimit_sleep
        wrapper.ratelimit_reset_time = ratelimit_reset_time
        wrapper.api_version = api_version

    def today_is_nationstates_birthday(self) -> bool:
        "Today is 11/13?"
        today = datetime.today()
        date: str = today.strftime('%D')
        birthday: bool = False
        if '11/13' in date:
            birthday = True
        return birthday

    def get_nationstates_age(self) -> str:
        "Current year - NationStates year of creation (NationStates was created in 2002)."
        created = 2002
        today = datetime.today().year
        age = today - created
        result = f'Around {age-1}-{age} years old.'
        return result

    def get_daily_data_dumps(self, filepath: str | Path = "./datadump.gz", type: str = "nation", **kwargs) -> None:
        """
        Dowloads NationStates daily data dumps.
        
        ### type: str
        
        - "nation": Dowloads the nation data dump.
        - "region": Dowloads the region data dump.
        - "cards": Dowloads the trading cards data dump, this one needs a `season_number: int`.
        """
        nation_url = url_manager.data_dumps_url("n")
        region_url = url_manager.data_dumps_url("r")
        cards_url = url_manager.data_dumps_url("c")
        
        query_parameters = {
            "downloadformat": "gz"
            }

        filepath = Path(filepath).absolute() 
        match type:
            case "n":
                with open(filepath, 'wb') as file:
                    response = wrapper.fetch_html_data(nation_url, query_parameters=query_parameters, stream=True)
                    for chunk in response.iter_content(chunk_size=10 * 1024):
                        file.write(chunk)
            case "r":
                with open(filepath, 'wb') as file:
                    response = wrapper.fetch_html_data(region_url, query_parameters=query_parameters, stream=True)
                    for chunk in response.iter_content(chunk_size=10 * 1024):
                        file.write(chunk)
            case "c":
                with open(filepath, 'wb') as file:
                    cards_url = cards_url.format(season_number=kwargs.get("season_number"))
                    response = wrapper.fetch_html_data(cards_url, query_parameters=query_parameters, stream=True)
                    for chunk in response.iter_content(chunk_size=10 * 1024):
                        file.write(chunk)
            case _:
                raise ValueError(type)

    def get_world_shards(self, shards: str | tuple | list = None, **kwargs) -> dict:
        """
        Gets one or more shards from the World API.
        """
        url = url_manager.shards_url("w").format(query=shards, params="")
        if shards:
            shards_query = join_keys([shard for shard in shards]) if type(shards) != str else shards
            shard_params = join_keys([f"{param}={kwargs[param]}" for param in kwargs], ";")            
            url = url_manager.shards_url("w")
            url = url.format(query = shards_query,
                            params = shard_params,)
        response = wrapper.fetch_api_data(url)
        return response

    def get_world_assembly_shards(self, council_id: int, shards: str | tuple | list = None, **kwargs) -> dict:
        """
        Gets one or more shards from the World Assembly API.
        """
        url = url_manager.shards_url("wa").format(council_id=1, query=shards, params="")
        if shards:
            shards_query = join_keys([shard for shard in shards]) if type(shards) != str else shards
            shard_params = join_keys([f"{param}={kwargs[param]}" for param in kwargs], ";")            
            url = url_manager.shards_url("wa")
            url = url.format(council_id = council_id,
                            query = shards_query,
                            params = shard_params)
        response = wrapper.fetch_api_data(url)
        return response

    class Nation:
        """
        Class dedicated to NationStates nation API.
        """
        def __init__(self, nation_name: str = 'testlandia') -> None:
            self.nation_name = format_key(nation_name, False, '%20')

        def exists(self) -> bool:
            """
            Checks if nation exists.
            """
            url = url_manager.generate_shards_url().format("nation", self.nation_name)
            status_code: int = wrapper.connection_status_code(url)
            match status_code:
                case 200:
                    return True
                case 404:
                    return False
                case _:
                    raise HTTPError(status_code)

        # Replacing get_public_shards()
        def get_shards(self, shards: str | tuple[str] | list[str] = None, **kwargs) -> dict:
            """
            Gets one or more public shards from the requested nation, returns the standard API by default.
            
            ### Standard:
            
            A compendium of the most commonly sought information.
            
            ### Shards:
            If you don't need most of this data, please use shards instead. Shards allow you to request exactly what you want and can be used to request data not available from the Standard API!
            """
            
            for kwarg in kwargs:
                if type(kwargs[kwarg]) != str:
                    kwargs[kwarg] = join_keys(kwargs[kwarg])
            params: str | None = join_keys([f"{kwarg}={kwargs[kwarg]}" for kwarg in kwargs], ";") if kwargs else None
            url = url_manager.generate_shards_url(shards, params)
            url = url.format("nation", self.nation_name)
            print(url)
            response = wrapper.fetch_api_data(url)
            return response

    class Region: 
        """
        Class dedicated to NationStates region API.
        """
        def __init__(self, region_name: str = 'The Pacific') -> None:
            self.region_name = format_key(region_name, False, '%20')
        
        def exists(self) -> bool:
            """
            Checks if region exists.
            """
            url = url_manager.generate_shards_url().format("region", self.region_name)
            status_code: int = wrapper.connection_status_code(url)
            match status_code:
                case 200:
                    return True
                case 404:
                    return False
                case _:
                    raise HTTPError(status_code)

        def get_shards(self, shards: str | tuple | list = None, **kwargs) -> dict:
            """
            Gets one or more shards from the requested region, returns the standard API by default.
            
            ### Standard:
            
            A compendium of the most commonly sought information.
            
            ### Shards:
            If you don't need most of this data, please use shards instead. Shards allow you to request exactly what you want and can be used to request data not available from the Standard API!
            """
            for kwarg in kwargs:
                if type(kwargs[kwarg]) != str:
                    kwargs[kwarg] = join_keys(kwargs[kwarg])
            params: str | None = join_keys([f"{kwarg}={kwargs[kwarg]}" for kwarg in kwargs], ";") if kwargs else None
            url = url_manager.generate_shards_url(shards, params)
            url = url.format("region", self.region_name)
            response = wrapper.fetch_api_data(url)
            return response

if __name__ == "__main__":
    api = AwesomeNations("AwesomeNations urllib3 test (by: Orlys; usdBy: Orlys)")
    nation = api.Nation("Orlys")
    region = api.Region("Fullworthia")
    
    data = nation.get_shards(["census", "fullname"], scale=(45, 32))
    pp(data)