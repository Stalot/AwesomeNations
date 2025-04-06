from awesomeNations import AwesomeNations

#  █████╗ ██╗    ██╗███████╗███████╗ ██████╗ ███╗   ███╗███████╗
# ██╔══██╗██║    ██║██╔════╝██╔════╝██╔═══██╗████╗ ████║██╔════╝
# ███████║██║ █╗ ██║█████╗  ███████╗██║   ██║██╔████╔██║█████╗  
# ██╔══██║██║███╗██║██╔══╝  ╚════██║██║   ██║██║╚██╔╝██║██╔══╝  
# ██║  ██║╚███╔███╔╝███████╗███████║╚██████╔╝██║ ╚═╝ ██║███████╗
# ╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝

# The result should be something like this:
# Name: Testlandia
# Full name: The Hive Mind of Testlandia
# WA category: Inoffensive Centrist Democracy
# Motto: New forum when?
# Region: Testregionia
# Influence: Powerbroker
#
# Civil Rights: Very Good
# Economy: Powerhouse
# Political Freedom: Excellent

api = AwesomeNations("My application/1.0.0") # Replace this User-Agent with useful info.

def search_nation():
    nation_name = str(input('Insert nation name: '))
    nation = api.Nation(nation_name)

    if not nation_name:
        output = r'¯\_(ツ)_/¯ Please, gimme a nation name!'
        return output
    elif not nation.exists():
        output = fr'"{nation_name}" not found!'
        return output

    api_data = nation.get_shards()
    data = api_data["nation"]
    output = f"""Name: {data["name"]}
Full name: {data["fullname"]}
WA category: {data["category"]}
Motto: {data["motto"]}
Region: {data["region"]}
Influence: {data["influence"]}

Civil Rights: {data["freedom"]["civilrights"]}
Economy: {data["freedom"]["economy"]}
Political Freedom: {data["freedom"]["politicalfreedom"]}"""
    return output

def main():
    result = search_nation()
    print(f'\n{result}')
    print("-"*60, end="\n")
    main()

# Testing whether our work was worth it... (Maybe not)
if __name__ == "__main__":
    main()