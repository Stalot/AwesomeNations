<p align="center">
  <img src="https://i.imgur.com/yQ9gI82.png" />
</p>

<h1 align="center">AwesomeNations</h1>	

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**AwesomeNations** is a clumsy Python library for scraping data from [NationStates](https://www.nationstates.net), a browser-based nation simulation game created at 13 November 2002 by Max Barry- Oh wait, nobody cares about real life lore. Anyways, this library allows you to collect nation and region data, retrieve census statistics, and much gore- more.

You can install AwesomeNations using pip:

``` bash
pip install awesomeNations
```

Easy, quick and almost make me forget I spent months of my life to make this thing work! **Help me**

---

### Nation Features: ദ്ദി(˵ •̀ ᴗ - ˵ ) ✧

You can get censuses from a nation doing this:

``` python
from awesomeNations import AwesomeNations as awn

nation = awn.Nation('testlandia')

AwesomeData = nation.get_census((0, 2, 4, 46, 88)) # Returns a generator object

for census in AwesomeData:
    print(census)
```

Output:

``` bash
{'id': 0, 'title': 'Civil Rights', 'value': '65.50', 'bubbles': {'world_rank': '95,716th', 'region_rank': '11th'}}
{'id': 2, 'title': 'Political Freedom', 'value': '70.86', 'bubbles': {'world_rank': '87,533rd', 'region_rank': '12th'}}
{'id': 4, 'title': 'Wealth Gaps', 'value': '1.41', 'bubbles': {'world_rank': '285,631st', 'region_rank': '43rd'}}
{'id': 46, 'title': 'Defense Forces', 'value': '7,512.87', 'bubbles': {'world_rank': '26,064th', 'region_rank': '12th'}}
{'id': 88, 'title': 'Food Quality', 'value': '139.90', 'bubbles': {'world_rank': '13,297th', 'region_rank': '6th'}}
```

Nation overview:

``` python
from awesomeNations import AwesomeNations as awn
from pprint import pprint as pp

nation = awn.Nation('testlandia')

overview = nation.get_overview()
pp(overview)
```

Output:

``` bash
{'box': {'animal': '★★★ nautilus ★★★',
         'capital': 'Tést City',
         'currency': 'Kro-bro-ünze',
         'faith': 'Neo-Violetism',
         'leader': 'Violet',
         'population': '46.479 billion'},
 'bubbles': {'civil_rights': 'Very Good',
             'economy': 'Powerhouse',
             'influence': 'Eminence Grise',
             'political_freedom': 'Excellent',
             'region': 'Testregionia'},
 'description': {'economy': 'The powerhouse Testlandian economy, worth a '
                            'remarkable 3,173 trillion Kro-bro-ünzes a year, '
                            'is driven almost entirely by government activity. '
                            'The industrial sector is solely comprised of the '
                            'Information Technology industry. Average income '
                            'is 68,285 Kro-bro-ünzes, and distributed '
                            'extremely evenly, with little difference between '
                            'the richest and poorest citizens.',
                 'government': 'The Hive Mind of Testlandia is a gargantuan, '
                               'genial nation, ruled by Violet with an even '
                               'hand, and renowned for its rum-swilling '
                               'pirates, hatred of cheese, and stringent '
                               'health and safety legislation. The '
                               'compassionate, democratic population of 46.479 '
                               'billion Testlandians have some civil rights, '
                               'but not too many, enjoy the freedom to spend '
                               'their money however they like, to a point, and '
                               'take part in free and open elections, although '
                               'not too often.\n'
                               'It is difficult to tell where the omnipresent '
                               'government stops and the rest of society '
                               'begins, but it juggles the competing demands '
                               'of Healthcare, Environment, and Education. It '
                               'meets to discuss matters of state in the '
                               'capital city of Tést City. The average income '
                               'tax rate is 88.9%, and even higher for the '
                               'wealthy.\n',
                 'more': "Political detractors refer to Violet as 'that "
                         "Bigtopian puppet', dubiously qualified Skandilundian "
                         "barristers keep referring to laws as 'government "
                         "guidelines', Violet's office has a newly installed "
                         'Max-Man arcade game programmed by a 5th-grader, and '
                         'Testlandians struggle to cut tofu steak with a '
                         'spoon. Crime is totally unknown, thanks to a very '
                         'well-funded police force and progressive social '
                         "policies in education and welfare.  Testlandia's "
                         'national animal is the ★★★ nautilus ★★★, which '
                         "frolics freely in the nation's sparkling oceans, and "
                         'its national religion is Neo-Violetism.'},
 'flag': 'www.nationstates.net/images/flags/uploads/testlandia__853435.png',
 'long_name': 'The Hive Mind of Testlandia',
 'motto': 'New forum when?',
 'short_name': 'Testlandia',
 'wa_category': 'Inoffensive Centrist Democracy'}
```

Activity:

``` python
from awesomeNations import AwesomeNations as awn

nation = awn.Nation('testlandia')

AwesomeActivity = nation.get_activity(filters='all') # Returns a generator object, None if no activities.

# Be aware that Testlandia is pretty sleepy recently, so they might be kinda inactive!
if AwesomeActivity:
    for event in AwesomeActivity:
        print(event)
else:
    print('No events.')
```

Output:

``` bash
4 days ago: Testlandia changed its national motto to "New forum when?".
5 days ago: Testlandia altered its national flag.
5 days ago: Testlandia altered its national flag.
```

### Region Features: ⸜(｡˃ ᵕ ˂ )⸝♡

Region overview:

``` python
from awesomeNations import AwesomeNations as awn
from pprint import pprint as pp

region = awn.Region('The Pacific')

overview = region.get_overview()
pp(overview)
```

Output:

``` bash
{'category': 'The Pacific is a Feeder. New nations are founded here at an '
             'elevated rate.',
 'founder': None,
 'governor': None,
 'last_wa_update': 'Last WA Update: 2 hours ago',
 'region_banner': 'https://www.nationstates.net/images/rbanners/uploads/the_pacific__638034.jpg',  
 'region_flag': 'https://www.nationstates.net/images/flags/uploads/rflags/the_pacific__176518.png',
 'wa_delegate': 'WA Delegate: The New Pacific Ocelot Empress of Xoriet '
                '(elected 157 days ago)'}
```

Get embassies from the desired region:

``` python
from awesomeNations import AwesomeNations as awn

region = awn.Region('The Pacific')

embassies = region.get_embassies()
for embassy in embassies:
    print(embassy)
```

Output:

``` bash
{'region': 'The New Pacific Order', 'duration': '9 years 84 days'}
{'region': 'The West Pacific', 'duration': '4 years 341 days'}
{'region': 'Lone Wolves United', 'duration': '1 year 352 days'}
{'region': 'The North Pacific', 'duration': '5 years 77 days'}
{'region': 'The East Pacific', 'duration': '9 years 132 days'}
{'region': 'Balder', 'duration': '5 years 133 days'}
{'region': 'Lazarus', 'duration': '2 years 134 days'}
{'region': 'Ridgefield', 'duration': '124 days'}
{'region': 'Anteria', 'duration': '122 days'}
{'region': 'Cape of Good Hope', 'duration': '124 days'}
{'region': 'Lands End', 'duration': '122 days'}
{'region': 'Conch Kingdom', 'duration': '124 days'}
{'region': 'Narnia', 'duration': '80 days'}
{'region': 'Dawn', 'duration': '70 days'}
{'region': 'The League', 'duration': '1 year 326 days'}
{'region': 'Atlantic', 'duration': '8 years 332 days'}
...
```

# Reference 三三ᕕ( ᐛ )ᕗ

**Nation Methods:**

- exists() -> bool: Check if a nation exists.
- get_overview() -> dict: Get an overview of a nation.
- get_activity() -> Iterator: Retrieve nation activity.
- get_census() -> Iterator: Retrieve census data.

**Region Methods:**

- exists() -> bool: Check if a region exists.
- get_overview() -> dict: Retrieve a region's overview.
- get_activity() -> Iterator: Retrieve world census rankings.
- get_embassies() -> Iterator: Get details about the region's embassies.