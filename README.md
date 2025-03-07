<p align="center">
  <img src="https://i.imgur.com/yQ9gI82.png" />
</p>

<h1 align="center">AwesomeNations</h1>

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**AwesomeNations** is a simple wrapper for [NationStates](https://www.nationstates.net), a browser-based nation simulation game created at 13 November 2002 by Max Barry- Oh wait, nobody cares about real life lore. Anyways, this library allows you to collect nation and region data, retrieve census statistics, and much gore- more.

You can install AwesomeNations using pip:

``` bash
pip install awesomeNations
```

Easy, quick and **awesome**.

## References: ദ്ദി(˵ •̀ ᴗ - ˵ ) ✧

I highly recommend you **dive into the NationStates documentation**. Yes, I know, it sounds as thrilling as watching paint dry... **But you really should**! Here are some handy links you might want to check out!

- [NationStates API documentation](https://www.nationstates.net/pages/api.html)
- [Script Rules for HTML site](https://forum.nationstates.net/viewtopic.php?p=16394966#p16394966)

## Summary 📚

**AwesomeNations**
- `get_api_latest_version()` -> Gets API current version;
- `get_daily_data_dumps()` -> Dowloads daily data dumps;
- `get_world_assembly_shards()` -> Gets world assembly shards;
- `get_world_shards()` -> Gets world API shards.

**Nation**
- `exists()` -> Checks if nation exists;
- `get_shards()` -> Gets nation API shards.

**Region**
- `exists()` -> Checks if region exists;
- `get_shards()` -> Gets region API shards.

## Nations 🚩

Let's begin with a simple example...

``` python
from awesomeNations import AwesomeNations
from pprint import pprint as pp # Pretty printing

api = AwesomeNations("My App/1.0.0 (by: Nation A, usedBy: Nation B)")
nation = api.Nation("Testlandia")

if nation.exists():
    data = nation.get_shards(["fullname", "leader", "religion", "capital", "currency"])
    pp(data)
```

Should provide something like:

``` bash
{'nation': {'capital': 'Tést City',
            'currency': 'Kro-bro-ünze',
            'fullname': 'The Hive Mind of Testlandia',
            'id': 'testlandia',
            'leader': 'Violet',
            'religion': 'Neo-Violetism'}}
```

Getting census...

``` python
if nation.exists():
    data = nation.get_shards("census", scale=(12, 0, 46)) # Use "all" to get all censuses!
    pp(data)
```

Returns:

``` python
{'nation': {'census': {'scale': [{'id': 0,
                                  'rank': 95822,
                                  'rrank': 12,
                                  'score': 66},
                                 {'id': 12,
                                  'rank': 334021,
                                  'rrank': 47,
                                  'score': -14.78},
                                 {'id': 46,
                                  'rank': 28478,
                                  'rrank': 10,
                                  'score': 7448.55}]},
            'id': 'testlandia'}}
```

## Regions 🌍

Same shard logic with regions!

``` python
from awesomeNations import AwesomeNations
from pprint import pprint as pp # Pretty printing

api = AwesomeNations("My App/1.0.0 (by: Nation A, usedBy: Nation B)")
region = api.Region("The Pacific")

if region.exists():
    data = region.get_shards("census", scale="all", mode="score")
    pp(data)
```

Provides:

``` bash
{'region': {'census': {'scale': [{'id': 0, 'score': 52.75},
                                 {'id': 1, 'score': 62.02},
                                 {'id': 2, 'score': 52.54},
                                 {'id': 3, 'score': 2888780000},
                                 {'id': 4, 'score': 10.91},
                                 {'id': 5, 'score': 37.11},
                                 {'id': 6, 'score': 44.11},
                                 ...
                                 {'id': 84, 'score': 67.06},
                                 {'id': 85, 'score': 39261.14},
                                 {'id': 86, 'score': 196.95},
                                 {'id': 87, 'score': 16.73},
                                 {'id': 88, 'score': 40.87}]},
            'id': 'the_pacific'}}
```