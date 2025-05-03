<h1 align="center">
  <img src="https://i.imgur.com/apn9Y52.png" alt="AwesomeNations Changelog logo"/>
</h1>

# </> 2.1.0 </>

What's new:

- **Nation** private commands;
- **Nation** `set_auth()`: Sets Nation authentication;
- Shard validation, to prevent user from requesting shards that don't exist;
- Overall internal organization upgrades.

# </> 2.0.0 </>

- **Nation** Authentication is now possible;
- **AwesomeNations** `get_daily_data_dumps()` now only accepts nation or region daily data dumps;
- **AwesomeNations** `get_nationstates_age()` now returns an int value.

Bug fixes:

- Problem while processing some numbers in XML response;
- Decoding error with certain API versions.

Deprecated methods:

- **Nation** `get_public_shards()` is deprecated and will be removed in next versions, use `get_shards()` instead.

New methods:

- **AwesomeNations** `get_api_latest_version()` gets API latest version.

Removed methods:

- **Nation** `get_summary()`.

# </> 1.0.0 </>

- Internal structure adapted from major **web scrapping** to **API wrapping**, this change was made to improve **efficiency** and better align with NationStates script rules;
- Documentation improved.

New methods:

- **AwesomeNations** `get_daily_data_dumps()`;
- **AwesomeNations** `get_world_shards()`;
- **AwesomeNations** `get_world_assembly_shards()`;
- **Nation** `get_summary()`;
- **Nation** `get_public_shards()`;
- **Region** `get_shards()`.

Modified methods:

- **AwesomeNations** `nationStates_birthday()` was renamed to `today_is_nationstates_birthday()`;
- **AwesomeNations** `nationStates_age()` was renamed to `get_nationstates_age()`.

Removed methods:

- **Nation** `get_overview()`;
- **Nation** `get_activity()`;
- **Nation** `get_census()`;
- **Region** `get_overview()`;
- **Region** `get_world_census()`;
- **Region** `get_activity()`;
- **Region** `get_embassies()`.

# </> 0.1.0 </>

- Region support;
- License addition;
- Scraping efficiency improvement;
- Changelog addition;
- Exceptions improvements;
- Code examples;
- Github repository creation;
- Less cringe.

# </> 0.0.4 </>

- First dummy release, hello... World...?
