# Awesome Changelog ≽^•⩊•^≼

# </> ?.?.? </>:

### Bug fixes:

- Problem while post processing complex numbers in XML response.

### Deprecated

-  **Nation**: get_summary();

# </> 1.0.0 </>:

- Internal structure adapted from major **web scrapping** to **API wrapping**, this change was made to improve **efficiency** and better align with NationStates script rules;
- Documentation improved.

New methods:
- **AwesomeNations**: get_daily_data_dumps()-> None;
- **AwesomeNations**: get_world_shards()-> dict;
- **AwesomeNations**: get_world_assembly_shards() -> dict;
- **Nation**: get_summary() -> dict;
- **Nation**: get_public_shards() -> dict;
- **Region**: get_shards() -> dict.

Modified methods:
- **AwesomeNations**: "nationStates_birthday()" was renamed to "today_is_nationstates_birthday()";
- **AwesomeNations**: "nationStates_age()" was renamed to "get_nationstates_age()".

Removed methods:
- **Nation**: get_overview();
- **Nation**: get_activity();
- **Nation**: get_census();
- **Region**: get_overview();
- **Region**: get_world_census();
- **Region**: get_activity();
- **Region**: get_embassies().

# </> 0.1.0 </>:

- Region support;
- License addition;
- Scraping efficiency improvement;
- Changelog addition;
- Exceptions improvements;
- Code examples;
- Github repository creation;
- Less cringe.

# </> 0.0.4 </>:

- First dummy release, hello... World...?