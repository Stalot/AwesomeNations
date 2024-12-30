from awesomeNations import AwesomeNations as awn

nation = awn.Nation('testlandia')

def man_power(defense_forces: float = 0, agriculture_sector: float = 0) -> int:
    output: int = max(1000, int((defense_forces) * (agriculture_sector / 100)))
    return output

def quality_of_life(lifespan: float, charmlessness: float) -> int:
    output: float = max(0, round(lifespan / charmlessness, 2))
    return output

def format_value(value: str):
    output = float(value.replace(',', ''))
    return output
def format_key(key: str):
    output = key.lower().replace(' ', '_').replace(':', '')
    return output

def main():
    data = list(nation.get_census([46, 17, 44, 64]))

    censuses = {}
    for census in data:
        censuses.update({format_key(census['title']): format_value(census['value'])})

    defense_forces = censuses['defense_forces']
    agriculture = censuses['sector_agriculture']
    lifespan = censuses['lifespan']
    charmlessness = censuses['charmlessness']

    result = man_power(defense_forces, agriculture)
    print(f'Man power: {result} active soldiers')
    result = quality_of_life(lifespan, charmlessness)
    print(f'Quality of life: {result}')

if __name__ == "__main__":
    main()