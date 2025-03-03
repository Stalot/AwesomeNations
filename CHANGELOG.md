<p align="center">
  <img src="https://i.imgur.com/apn9Y52.png" #gh-light-mode-only/>
  <img src="https://i.imgur.com/6brBjtZ.png" #gh-dark-mode-only/>
</p>

## </> 2.0.0 </>:

- Nation authentication for private shards;
- Data structure

### Current Dependencies:

There are some dependency changes in version 2.0.0, here are the current dependencies you need to worry about when using AwesomeNations!

| Library                | Dependency         |
| -----------------------| ------------------ |
|  beautifulsoup4        | :x:                |
|  requests              | :x:                |
|  lxml                  | :x:                |
|  urllib3               | :white_check_mark: |
|  xmltodict             | :white_check_mark: |

### Deprecated:
- **Nation**: `get_public_shards()` is deprecated and will be removed in next versions, use `get_shards()` instead.

### Removed:
- **Nation**: `get_summary()`.

### Bug fixes:
- Problem while post processing complex numbers in XML response.

## </> 1.0.0 </>:

- Internal structure adapted from major **web scrapping** to **API wrapping**, this change was made to improve **efficiency** and better align with NationStates script rules;
- Documentation improved.

### New methods:
- **AwesomeNations**: `get_daily_data_dumps()`;
- **AwesomeNations**: `get_world_shards()`;
- **AwesomeNations**: `get_world_assembly_shards()`;
- **Nation**: `get_summary()`;
- **Nation**: `get_public_shards()`;
- **Region**: `get_shards()`.

### Modified methods:
- **AwesomeNations**: `nationStates_birthday()` was renamed to `today_is_nationstates_birthday()`;
- **AwesomeNations**: `nationStates_age()` was renamed to `get_nationstates_age()`.

### Removed methods:
- **Nation**: `get_overview()`;
- **Nation**: `get_activity()`;
- **Nation**: `get_census()`;
- **Region**: `get_overview()`;
- **Region**: `get_world_census()`;
- **Region**: `get_activity()`;
- **Region**: `get_embassies()`.

## </> 0.1.0 </>:

- Region support;
- License addition;
- Scraping efficiency improvement;
- Changelog addition;
- Exceptions improvements;
- Code examples;
- Github repository creation;
- Less cringe.

## </> 0.0.4 </>:

- First dummy release, hello... World...?