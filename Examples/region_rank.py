from awesomeNations import AwesomeNations

#  █████╗ ██╗    ██╗███████╗███████╗ ██████╗ ███╗   ███╗███████╗
# ██╔══██╗██║    ██║██╔════╝██╔════╝██╔═══██╗████╗ ████║██╔════╝
# ███████║██║ █╗ ██║█████╗  ███████╗██║   ██║██╔████╔██║█████╗  
# ██╔══██║██║███╗██║██╔══╝  ╚════██║██║   ██║██║╚██╔╝██║██╔══╝  
# ██║  ██║╚███╔███╔╝███████╗███████║╚██████╔╝██║ ╚═╝ ██║███████╗
# ╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝

api = AwesomeNations("Region score rank example") # Replace this User-Agent with useful info.
region = api.Region('The Pacific')

def pretty_name(name: str) -> str:
    name = name.replace("_", " ").split(" ")
    name = [word.capitalize() for word in name]
    name = " ".join(name)
    return name

def pretty_rank(rank_number: str, digits: int = 2) -> str:
    rank_number = str(rank_number)
    i = digits
    while i > 0:
        rank_number = "0" + rank_number if len(rank_number) < digits else rank_number
        i -= 1
    return rank_number

def get_region_rank(censusid: int = 46, max_position: int = 10):
    api_data = region.get_shards("censusranks", scale=censusid)
    rank_data = api_data["region"]["censusranks"]["nations"]["nation"]
    api_data = api.get_world_shards("censusname", scale=censusid)
    census_title = api_data["world"]["census"]["text"]

    if max_position <= 0:
        raise ValueError(f"Value: {max_position}, rank positions must be positive! (and above zero.)")

    print(f"Region's {census_title} rank:\n")

    for rank in rank_data:
        nation_rank = pretty_rank(rank["rank"], len(str(max_position)))
        nation_name: str = pretty_name(rank["name"])
        nation_score = rank["score"]

        if int(nation_rank) > max_position:
            break

        msg = f"{nation_rank} - {nation_name}\nScore: {nation_score}"
        print(msg, "\n" + "="*30)

get_region_rank()