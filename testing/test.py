from awesomeNations import AwesomeNations as awn
import json

if __name__ == '__main__':
    nation = awn.Nation
    census = nation("Testlandia").get_census([0])
    json_data = json.dumps(census)

    with open('data.json', 'w') as f:
        f.write(json_data)