# AwesomeNations

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**AwesomeNations** is a lightweight Python library for scraping data from [NationStates](https://www.nationstates.net), a browser-based nation simulation game. It allows you to collect nation and region data, retrieve census statistics, and much more.

## Features
- **Nation Data**: Retrieve overviews, census statistics, and existence checks for any nation.
- **Region Data**: Get details like world census ranks, embassies, and other regional information.

---

## Installation

Install AwesomeNations using pip:

``` bash
pip install awesomeNations
```

## Quick Start

Here’s how to start using AwesomeNations:

**Nation Features**

Checking if a nation exists:
``` python
from awesomeNations import AwesomeNations as awn

nation = awn.Nation
print(nation("testlandia").exists())  # Output: True or False
```

Getting nation overview:
``` python
from awesomeNations import AwesomeNations as awn

nation = awn.Nation
overview = nation("testlandia").get_overview()
print(overview)
```
Output (json):
``` json
{
    "flag": "www.nationstates.net/images/flags/uploads/testlandia__656619.svg",
    "short_name": "Testlandia",
    "long_name": "The Hive Mind of Testlandia",
    "wa_category": "Inoffensive Centrist Democracy",
    "motto": "Fixed, thanks.",
    ...
}
```

Retrieve census data:
``` python
from awesomeNations import AwesomeNations as awn

nation = awn.Nation
census_data = nation("testlandia").get_census([0])
print(census_data)
```
Output (json):
``` json
{
    "civil_rights": {
        "title": "Civil Rights",
        "raw_value": "65.50",
        "value": 65.5, "bubbles": {"world_rank": "96,648th", "region_rank": "11th"}
        }
}
```

**Region Features**

Check if a region exists:
``` python
from awesomeNations import AwesomeNations as awn

region = awn.Region
print(region("The Pacific").exists())  # Output: True or False
```

Retrieve region overview:
``` python
from awesomeNations import AwesomeNations as awn

region = awn.Region
overview = region("The Pacific").get_overview()
print(overview)
```

Retrieve region world census:
``` python
from awesomeNations import AwesomeNations as awn

region = awn.Region
rank = region("The Pacific").get_world_census(censusid=46)
print(rank)
```
Output (json):
``` json
{
    "title": "The Most Advanced Defense Forces in the Pacific",
    "description": "Nations ranked highly spend the most on national defense, and are most secure against foreign aggression.",
    "region_world_rank": "As a region, the Pacific is ranked 5,861st in the world for Most Advanced Defense Forces.",
    "rank": [...]
}
```

# Reference

**Nation Methods:**

- exists() -> bool: Check if a nation exists.
- get_overview() -> dict: Get an overview of a nation.
- get_census(censusid: list) -> dict: Retrieve census data.

**Region Methods:**

- exists() -> bool: Check if a region exists.
- get_overview() -> dict: Retrieve a region's overview.
- get_world_census(censusid: int) -> dict: Retrieve world census rankings.
- get_embassies() -> dict: Get details about the region's embassies.