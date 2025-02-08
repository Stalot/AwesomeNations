from awesomeNations import AwesomeNations

#  █████╗ ██╗    ██╗███████╗███████╗ ██████╗ ███╗   ███╗███████╗
# ██╔══██╗██║    ██║██╔════╝██╔════╝██╔═══██╗████╗ ████║██╔════╝
# ███████║██║ █╗ ██║█████╗  ███████╗██║   ██║██╔████╔██║█████╗  
# ██╔══██║██║███╗██║██╔══╝  ╚════██║██║   ██║██║╚██╔╝██║██╔══╝  
# ██║  ██║╚███╔███╔╝███████╗███████║╚██████╔╝██║ ╚═╝ ██║███████╗
# ╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝

awesomeAPI = AwesomeNations("My ultra omega super blaster cool application")

def main():
    try:
        censusid = int(input("insert census id: "))
        
        world_api_data: dict = awesomeAPI.get_world_shards(["censusname", "censusdesc"], scale=censusid)
        census_description: dict = world_api_data["world"]["censusdesc"]
        
        nation_census_description: str = "No description available."
        region_census_description: str = "No description available."
        census_name: str = "Not found."

        census_title: dict = world_api_data["world"]["census"].get("text")
        if census_title:
            census_name = census_title
            nation_census_description = census_description["ndesc"]
            region_census_description = census_description["rdesc"]
        
        msg = f"\n{census_name}\n{"="*40}\n{nation_census_description}\n---\n{region_census_description}\n"
        print(msg)
        main()
    except ValueError as v_error:
        print(f"\n{v_error}\nPlease, insert a valid number!\n")
        main()

main()