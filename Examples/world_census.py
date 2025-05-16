from awesomeNations import AwesomeNations
from typing import Any, Optional

#  █████╗ ██╗    ██╗███████╗███████╗ ██████╗ ███╗   ███╗███████╗
# ██╔══██╗██║    ██║██╔════╝██╔════╝██╔═══██╗████╗ ████║██╔════╝
# ███████║██║ █╗ ██║█████╗  ███████╗██║   ██║██╔████╔██║█████╗  
# ██╔══██║██║███╗██║██╔══╝  ╚════██║██║   ██║██║╚██╔╝██║██╔══╝  
# ██║  ██║╚███╔███╔╝███████╗███████║╚██████╔╝██║ ╚═╝ ██║███████╗
# ╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝

api = AwesomeNations("World census searcher example") # Replace this User-Agent with useful info.

def main():
    censusid: str | int = input("insert census id: ")
    if not censusid.isdigit():
        print(f"Please, insert a valid number!\n")
        main()
    censusid = int(censusid)
    
    world_api_data: dict[str, dict[str, Any]] = api.get_world_shards(["censusname", "censusdesc"], scale=censusid)
    census_description: dict[str, str] = world_api_data["world"]["censusdesc"]
    
    nation_census_description: str = "No description available."
    region_census_description: str = "No description available."
    census_name: str = "Not found."

    census_title: Optional[str] = world_api_data["world"]["census"].get("text")
    if census_title:
        census_name: str = census_title
        nation_census_description: str = census_description["ndesc"]
        region_census_description: str = census_description["rdesc"]
    
    msg: str = f"\n{census_name}\n{"="*40}\n{nation_census_description}\n---\n{region_census_description}\n"
    print(msg)
    main()

main()