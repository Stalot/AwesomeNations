from awesomeNations import AwesomeNations as awn
from pathlib import Path
import json

nation = awn.Nation

# Gets one or more censuses based on your id.
def get_cool_census(nation_name: str = 'testlandia'):
    if nation(nation_name).exists():
        overview = nation(nation_name).get_census([0, 46, 72, 88])
        return overview
    else:
        return "Nation not found."

# Creates a json file in a new folder.
def create_file(data):
    cwd = Path.cwd()
    output_path = cwd / 'Output'
    if not output_path.exists():
        Path.mkdir(output_path)

    json_format = json.dumps(data)
    with open(output_path / 'census.json', 'w') as file:
        file.write(json_format)
    print(f'\nJson file successfully created at: {output_path}')

def main():
    data = get_cool_census()
    if data != 'Nation not found.':
        create_file(data)
    else:
        print(f'{data}\n')

if __name__ == '__main__':
    main()