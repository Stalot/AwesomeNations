from awesomeNations import AwesomeNations as awn

region = awn.Region('The Pacific')

embassies = region.get_embassies()
for embassy in embassies:
    print(embassy)