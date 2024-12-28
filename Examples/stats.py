from awesomeNations import AwesomeNations as awn
from pprint import pprint as pp

nation = awn.Nation('testlandia')
data = nation.get_census([46, 17, 44, 64])

def man_power(defense_forces: float = 0, agriculture_sector: float = 0) -> int:
    output: int = max(1000, int((defense_forces) * (agriculture_sector / 100)))
    return output

def quality_of_life(lifespan: float, charmlessness: float) -> int:
    output: int = int(lifespan / charmlessness)
    return output


result = man_power(data['defense_forces']['value'], data['sector_agriculture']['value'])
print(f'Man power: {result} active soldiers')
result = quality_of_life(data['lifespan']['value'], data['charmlessness']['value'])
print(f'Quality of life: {result}')