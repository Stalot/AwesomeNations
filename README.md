# AwesomeNations

AwesomeNations is a simple python web scraping library for NationStates. Useful to get nation census like Defense Forces, Compassion, Scientific Advancement and etc.


# How to play!

Getting nation census:
``` python
from awesomeNations import AwesomeNations as awn

data = awn.get_census('testlandia', [46, 74])
print(data)
```

Returns:
`{'defense_forces': '7,425.68', 'average_income_of_rich': '79,619'}`

Changing the "raw" argument (True by default):
``` python
from awesomeNations import AwesomeNations as awn

data = awn.get_census('testlandia', [46, 74], raw=False)
print(data)
```

Returns:
`{'defense_forces': 7425.68, 'average_income_of_rich': 79619}`