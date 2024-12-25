from awesomeNations import AwesomeNations as awn

# Result should be something like:

# Short name: Testlandia
# Long name: The Hive Mind of Testlandia
# WA category: Inoffensive Centrist Democracy
# Motto: Fixed, thanks.
# Region: Testregionia
# Influence: Eminence Grise

def check_nation():
    nation_name = str(input('Insert nation name: '))
    nation = awn.Nation(nation_name)

    if not nation.exists():
        output = fr'"{nation_name}" ¯\_(ツ)_/¯'
        return output

    data = nation.get_overview()
    output = f"""Short name: {data['short_name']}
Long name: {data['long_name']}
WA category: {data['wa_category']}
Motto: {data['motto']}
Region: {data['bubbles']['region']}
Influence: {data['bubbles']['influence']}"""
    return output

def main():
    result = check_nation()
    print(f'\n{result}\n')
    main()

# Testing whether our work was worth it... (Maybe not)
if __name__ == "__main__":
    main()