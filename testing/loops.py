names = ['equestria', 'URSS', 'Brazil', 'China']
durations = ['2m', '12m', '1h:34m', '34m']

data = (item for item in (names, durations))

for stuff in data:
    print(stuff)