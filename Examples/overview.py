from awesomeNations import AwesomeNations as awn

# The result should be something like:

# Short name: Testlandia
# Long name: The Hive Mind of Testlandia
# WA category: Inoffensive Centrist Democracy
# Motto: Fixed, thanks.
# Region: Testregionia
# Influence: Eminence Grise
#
# Civil Rights: Very Good
# Economy: Powerhouse
# Political Freedom: Excellent

def search_nation():
    nation_name = str(input('Insert nation name: '))
    nation = awn.Nation(nation_name)

    if not nation_name:
        output = r'¯\_(ツ)_/¯ Please, gimme a natiom name!'
        return output
    elif not nation.exists():
        output = fr'"{nation_name}" not found. ¯\_(ツ)_/¯'
        return output

    data = nation.get_overview()
    output = f"""Short name: {data['short_name']}
Long name: {data['long_name']}
WA category: {data['wa_category']}
Motto: {data['motto']}
Region: {data['bubbles']['region']}
Influence: {data['bubbles']['influence']}

Civil Rights: {data['bubbles']['civil_rights']}
Economy: {data['bubbles']['economy']}
Political Freedom: {data['bubbles']['political_freedom']}"""
    return output

def main():
    result = search_nation()
    print(f'\n{result}\n')
    main()

# Testing whether our work was worth it... (Maybe not)
if __name__ == "__main__":
    main()