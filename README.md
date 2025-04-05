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

Before start *cooking*, I highly recommend you **dive into documentation**. Yes, I know, it sounds as thrilling as watching paint dry... **But you really should**!

- [NationStates API documentation](https://www.nationstates.net/pages/api.html)
- [Script Rules for HTML site](https://forum.nationstates.net/viewtopic.php?p=16394966#p16394966)

## Summary 📚

**AwesomeNations**
- `get_api_latest_version()` -> Gets API latest version;
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

api = AwesomeNations("My App/1.0.0")
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
                                  'rank': 97963,
                                  'rrank': 12,
                                  'score': 65.44},
                                 {'id': 12,
                                  'rank': 326811,
                                  'rrank': 46,
                                  'score': -14.3},
                                 {'id': 46,
                                  'rank': 28725,
                                  'rrank': 11,
                                  'score': 7432.07}]},
            'id': 'testlandia'}}
```

Now, let's see what truly separates little boys from grown men: **private shards!**

**NOTE:** It's strongly recommended to use [environment variables](https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1) to keep your dirty secrets... Secrets. The example below uses [python-dotenv](https://pypi.org/project/python-dotenv/) to prevent bad people like you or my mother-in-law from hacking my account! :D

``` python
from awesomeNations import AwesomeNations
from dotenv import load_dotenv
from pprint import pp
import os

# Get sensitive data from .env file
load_dotenv()
password = os.environ["MY_PASSWORD"]

api = AwesomeNations("My application/1.0.0") # Replace this User-Agent with useful info.
nation = api.Nation("your nation name here!", password)

data = nation.get_shards(('notices', 'ping', 'unread'))
pp(data)
```

Meanwhile in the .env file... Let's say your password is *"coolSkeleton98"*:

`MY_PASSWORD = "coolSkeleton98"`

## Regions 🌍

Same shard logic with regions!

``` python
from awesomeNations import AwesomeNations
from pprint import pprint as pp # Pretty printing

api = AwesomeNations("My App/1.0.0")
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