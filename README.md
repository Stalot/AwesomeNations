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

## Getting shards: ദ്ദി(˵ •̀ ᴗ - ˵ ) ✧

- [Nation shards](https://www.nationstates.net/pages/api.html#nationapi-publicshards)
- [Region shards](https://www.nationstates.net/pages/api.html#regionapi-shards)
- [World shards](https://www.nationstates.net/pages/api.html#worldapi-shards)
- [World Assembly shards](https://www.nationstates.net/pages/api.html#waapi-shards)

## Nations 🚩

Well, well, well... So you want some nation shards, huh? Take a look on the bashes below then! Let's start with a simple example...

```python
from awesomeNations import AwesomeNations
from pprint import pprint as pp # Normal printing, but more pretty!

awn = AwesomeNations("My Awesome App/0.0.1 (by:Testlandia; usedBy:Maxtopia)") # Put useful info here.
nation = awn.Nation

shards_list = ("name", "fullname", "motto", "leader", "religion")
nation_shards_data = nation("testlandia").get_public_shards(shards_list)
pp(nation_shards_data)
```

Returns this beauty:

``` bash
{'nation': {'fullname': 'The Hive Mind of Testlandia',
            'id': 'testlandia',
            'leader': 'Violet',
            'motto': 'New forum when?',  
            'name': 'Testlandia',        
            'religion': 'Neo-Violetism'}}
```

Now lets try to **get a census**...

``` python
nation_censuses_data = nation("testlandia").get_public_shards("census", scale=46)
print(nation_censuses_data)
```

Retrives:

``` bash
{'nation': {'id': 'testlandia', 'census': {'scale': {'id': 46, 'score': 7493.24, 'rank': 27809, 'rrank': 10}}}}
```

Cool, but don't feel Enough... Let's checkout **all censuses**!!!

``` python
nation_censuses_data = nation("testlandia").get_public_shards("census", scale="all")
pp(nation_censuses_data)
```

Retrives:

``` bash
{'nation': {'census': {'scale': [{'id': 0,
                                  'rank': 96913,  
                                  'rrank': 11,    
                                  'score': 66},   
                                 {'id': 1,        
                                  'rank': 78719,  
                                  'rrank': 21,    
                                  'score': 92.85},
                                 {'id': 2,        
                                  'rank': 89184,  
                                  'rrank': 11,    
                                  'score': 71.43},
                                 {'id': 3,        
                                  'rank': 396,
                                  'rrank': 1,
                                  'score': 46656000000},
                                 {'id': 4,
                                  'rank': 311489,
                                  'rrank': 39,
                                  'score': 1.4},
                                 {'id': 5,
                                  'rank': 333262,
                                  'rrank': 41,
                                  'score': 20.28},
                                 {'id': 6,
                                  'rank': 52002,
                                  'rrank': 10,
                                  'score': 46.76},
                                 {'id': 7,
                                  'rank': 1355,
                                  'rrank': 2,
                                  'score': 14879.42},
                                 {'id': 8,
                                  'rank': 247267,
                                  'rrank': 35,
                                  'score': 42},
                                 {'id': 9,
                                  'rank': 162457,
                                  'rrank': 22,
                                  'score': 128.5},
                                 {'id': 10,
                                  'rank': 342378,
                                  'rrank': 44,
                                  'score': -24.82},
                                 {'id': 11,
                                  'rank': 342074,
                                  'rrank': 43,
                                  'score': -13.15},
                                 {'id': 12,
                                  'rank': 343280,
                                  'rrank': 44,
                                  'score': -14.87},
                                 {'id': 13,
                                  'rank': 162162,
                                  'rrank': 25,
                                  'score': 3237.08},
                                 {'id': 14,
                                  'rank': 313062,
                                  'rrank': 40,
                                  'score': -10.67},
                                 {'id': 15,
                                  'rank': 335589,
                                  'rrank': 43,
                                  'score': -12.9},
                                 {...}]},
            'id': 'testlandia'}}
```

**Getting nation summary**: (Text from the requested nation [page](https://www.nationstates.net/nation=testlandia)!)

``` python
nation_summary = nation("testlandia").get_summary()
pp(nation_summary)
```

Should return something like:

``` python
{'description': {'economy': 'The powerhouse Testlandian economy, worth a '
                            'remarkable 3,202 trillion Kro-bro-ünzes a year, '  
                            'is driven almost entirely by government activity. '
                            'The industrial sector is solely comprised of the ' 
                            'Information Technology industry. Average income '  
                            'is 68,642 Kro-bro-ünzes, and distributed '
                            'extremely evenly, with little difference between ' 
                            'the richest and poorest citizens.',
                 'government': 'It is difficult to tell where the omnipresent ' 
                               'government stops and the rest of society '      
                               'begins, but it juggles the competing demands '  
                               'of Healthcare, Environment, and Education. It ' 
                               'meets to discuss matters of state in the '      
                               'capital city of Tést City. The average income '
                               'tax rate is 89.1%, and even higher for the '
                               'wealthy.',
                 'legislation': 'Dubiously qualified Skandilundian barristers '
                                "keep referring to laws as 'government "
                                "guidelines', Violet's office has a newly "
                                'installed Max-Man arcade game programmed by a '
                                '5th-grader, Testlandians struggle to cut tofu '
                                'steak with a spoon, and girls who wear '
                                'lipstick are berated for pandering to male '
                                'gazes. Crime is totally unknown, thanks to a '
                                'very well-funded police force and progressive '
                                'social policies in education and welfare.  '
                                "Testlandia's national animal is the ★★★ "
                                'nautilus ★★★, which frolics freely in the '
                                "nation's sparkling oceans, and its national "
                                'religion is Neo-Violetism.',
                 'society': 'The Hive Mind of Testlandia is a gargantuan, safe '
                            'nation, ruled by Violet with a fair hand, and '
                            'renowned for its museums and concert halls, '
                            'hatred of cheese, and stringent health and safety '
                            'legislation. The compassionate, democratic '
                            'population of 46.656 billion Testlandians are '
                            'fiercely patriotic and enjoy great social '
                            'equality; they tend to view other, more '
                            'capitalist countries as somewhat immoral and '
                            'corrupt.'}}
```

## Regions 🌍

Same shard logic apply to regions:

``` python
region = awn.Region
region_shards = region("The EAST pacific").get_shards()
pp(region_shards)
```

Should return something like this:

``` bash
{'region': {'banner': 808732,
            'bannerurl': '/images/rbanners/uploads/the_east_pacific__808732.jpg',
            'delegate': 'american-cascadia',
            'delegateauth': 'XWABCEP',
            'delegatevotes': 449,
            'embassies': {'embassy': ['Japan',
                                      'The Glorious Nations of Iwaku',
                                      'Yggdrasil',
                                      'Eientei Gensokyo',
                                      'Thaecia',
                                      'Equiterra',
                                      'The Free Nations Region',
                                      'the Pacific',
                                      'The Region That Has No Big Banks',
                                      'Europeia',
                                      'the South Pacific',
                                      '10000 Islands',
                                      'the Rejected Realms',
                                      'The Union of Democratic States',
                                      'The North Pacific',
                                      'Balder',
                                      'Lazarus',
                                      'Conch Kingdom',
                                      'Refugia',
                                      'Lone Wolves United',
                                      'The Black Hawks',
                                      'Carcassonne',
                                      'Caer Sidi',
                                      'The Land of Kings and Emperors',
                                      'The Kingdom of Great Britain',
                                      'The Social Liberal Union',
                                      'Democratic Socialist Assembly',
                                      'Warzone Asia',
                                      'The Hole To Hide In',
                                      'Palmetto',
                                      'Anime Nations Against Liberals',
                                      'Hyrule',
                                      'Pasridi Confederacy',
                                      'Worlds to Build',
                                      'Confederated East Pacific',
                                      {'text': 'Adairidae',
                                       'type': 'invited'}]},
            'factbook': '&amp;#128227; '
                        '[b][color=#359C46]W[/color][color=#339A48]e[/color][color=#32984B]l[/color][color=#31964D]c[/color][color=#309450]o[/color][color=#2E9353]m[/color][color=#2D9155]e[/color] '
                        '[color=#2B8D5A]t[/color][color=#298C5D]o[/color] '
                        '[color=#278862]T[/color][color=#268665]h[/color][color=#248467]e[/color] '
                        '[color=#29885F]E[/color][color=#2B895B]a[/color][color=#2D8B57]s[/color][color=#2F8C53]t[/color] '
                        '[color=#338F4A]P[/color][color=#359146]a[/color][color=#379242]c[/color][color=#39943E]i[/color][color=#3B953A]f[/color][color=#3D9736]i[/color][color=#409931]c[/color][/b] '
                        '- '
                        '[b][i][color=#27ceff]T[/color][color=#27c4ff]h[/color][color=#27beff]e[/color] '
                        '[color=#27b4ff]p[/color][color=#27aaff]l[/color][color=#279aff]a[/color][color=#278cff]c[/color][color=#277fff]e[/color] '
                        '[color=#276fff]o[/color][color=#2765ff]f[/color] '
                        '[color=#275bff]y[/color][color=#2765ff]o[/color][color=#276fff]u[/color][color=#277fff]r[/color] '
                        '[color=#278cff]d[/color][color=#279aff]r[/color][color=#27aaff]e[/color][color=#27b4ff]a[/color][color=#27beff]m[/color][color=#27c4ff]s[/color][color=#27ceff]![/color] '
                        '[/i][/b]\n'
                        '\n'
                        '[hr]\n'
                        '\n'
                        '&amp;#128262; '
                        '[b][url=https://discord.gg/qhDtwr9][color=#008026]Discord[/color][/url] '
                        '&amp;#128262; '
                        '[url=https://forum.theeastpacific.com/][color=#96b819]Forums[/color][/url] '
                        '&amp;#128262; '
                        '[url=https://www.nationstates.net/page=dispatch/id=2599456][color=#008026]Regional '      
                        'Newspaper[/color][/url] &amp;#128262; '
                        '[url=https://www.nationstates.net/page=dispatch/id=1861129][color=#96b819]Valsora '       
                        '- Official RMB Map[/color][/url] &amp;#128262; '
                        '[url=https://www.nationstates.net/page=dispatch/id=2598695][color=#008026]RMB '
                        'Rules[/color][/url]  &amp;#128262; '
                        '[url=https://www.nationstates.net/page=dispatch/id=2598687][color=#96b819]Foreign '       
                        'Affairs Handbook[/color][/url][/b] &amp;#128262; '
                        '[url=https://www.nationstates.net/page=dispatch/id=2508943][b][color=#008026]Regional '   
                        'Military[/color][/b][/url] &amp;#128262;\n'
                        '\n'
                        '[hr]\n'
                        '\n'
                        '&amp;#127891; [b][color=#1C6F34]New Arrivals '
                        'Guide[/color][/b]\n'
                        '\n'
                        'Check out the '
                        '[url=https://www.nationstates.net/page=dispatch/id=2598700][u][b]STEP[/b][/u][/url] '     
                        'program - The East Pacific&#146;s official welcome '
                        'guide!\n'
                        '\n'
                        '[hr]\n'
                        '\n'
                        '\n'
                        '&amp;#9888;&amp;#65039; [color=#1C6F34][b]Endorsement '
                        'Cap: 300[/b][/color]\n'
                        '\n'
                        'Please join the '
                        '[b][url=https://www.nationstates.net/page=un]World '
                        'Assembly[/url][/b] and endorse Delegate '
                        '[b][nation]American-Cascadia[/nation][/b] and the '
                        '[url=https://www.nationstates.net/page=dispatch/id=2598693][b]Viziers![/b][/url]\n'       
                        '\n'
                        '[hr]\n'
                        '\n'
                        '&amp;#128202; [color=#1C6F34][b]World Assembly '
                        'Recommendations:[/b][/color]\n'
                        '\n'
                        '[list]\n'
                        '\n'
                        '[*]General Assembly: [color=green][b]FOR[/b][/color]\n'
                        '[*]Security Council: [color=green][b]FOR[/b][/color]\n'
                        '\n'
                        '[/list]\n'
                        '\n'
                        '[hr]\n'
                        '\n'
                        '&amp;#129351; [color=#1C6F34][b]RMB Quote of the '
                        'Day:[/b][/color]\n'
                        '[quote=royabad;58334693]surely this&#146;ll bring '
                        'down the price of eggs[/quote]\n'
                        '\n'
                        '\n'
                        '[hr]\n'
                        '\n'
                        '&amp;#128240; [color=#1C6F34][b]News '
                        'Bulletin:[/b][/color][list]\n'
                        '\n'
                        '[*][b][u][url=https://www.nationstates.net/page=dispatch/id=2599456]Our '
                        'December 2024 EPNS edition has '
                        'launched![/url][/u][/b] Click and upvote!\n'
                        '[*]Dispatches have been recovered and placed back in '
                        'the WFE.',
            'flag': 'https://www.nationstates.net/images/flags/uploads/rflags/the_east_pacific__744779.png',       
            'founder': 0,
            'frontier': 0,
            'governor': 0,
            'lastmajorupdate': 1738651173,
            'lastminorupdate': 1738691727,
            'lastupdate': 1738691727,
            'name': 'The East Pacific',
            'nations': {...},
            'numnations': 5541,
            'officers': {...},
            'power': 'Extremely High'}}
```

## Summary

**AwesomeNations**
- get_daily_data_dumps() -> None: Dowloads daily data dumps;
- get_world_shards() -> dict: Gets the World API shards;
- get_world_assembly_shards() -> dict: Gets the World Assembly API shards.

**Nation**
- exists() -> bool: Checks if nation exists;
- get_public_shards() -> dict: Gets Nation API public shards;
- get_summary() -> dict: Gets the nation summary (from it's respective NationStates page).

**Region**
- exists() -> bool: Checks if region exists;
- get_shards() -> dict: Gets region shards.

---
---