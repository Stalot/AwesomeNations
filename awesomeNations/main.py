from awesomeNations.objects import NationObject, RegionObject
from datetime import datetime

class AwesomeNations:
    def nationStates_birthday() -> bool:
        "Today is 11/13?"
        today = datetime.today()
        date: str = today.strftime('%D')
        birthday: bool = False
        if '11/13' in date:
            birthday = True
        return birthday

    def nationStates_age() -> str:
        "Current year - NationStates year of creation (NationStates was created in 2002)."
        created = 2002
        today = datetime.today().year
        age = today - created
        result = f'Around {age-1}-{age} years old.'
        return result

    class Nation:
        """
        Class dedicated to extracting data from NationStates nations.
        """
        def __init__(self, nation_name: str = 'testlandia') -> None:
            self.nation_name = nation_name

        def exists(self) -> bool:
            """
            Checks if nation exists.
            """
            exist = NationObject.exists(self)
            return exist
        
        def get_overview(self) -> dict:
            """
            Get an overview of the requested nation.
            """
            overview = NationObject.overview(self)
            return overview

        def get_census(self, censusid: list = [0]) -> dict:
            """
            Gets one or more censuses [0-88] from the requested nation, examples:
            - [0]: Civil rights
            - [46]: Defense Forces
            - [0, 1, 2, 3] ... [88]
            """
            census = NationObject.census(self, censusid)
            return census

    class Region:
        """
        Class dedicated to extracting data from NationStates regions.
        """
        def __init__(self, region_name: str = 'The Pacific') -> None:
            self.region_name = region_name
        
        def exists(self) -> bool:
            """
            Checks if the region exists.
            """
            exist = RegionObject.exists(self)
            return exist
        
        def get_overview(self) -> dict:
            """
            Provides an overview of the requested region.
            """
            overview = RegionObject.overview(self)
            return overview

        def get_world_census(self, censusid: int) -> dict:
            """
            Retrieves the world census rankings for the requested region.
            """
            ranks = RegionObject.world_census(self, censusid)
            return ranks

        def get_embassies(self) -> dict:
            """
            Retrieves the embassies of the requested region.
            """
            embassies = RegionObject.embassies(self)
            return embassies


# Testing to see if my life is worth it:
if __name__ == '__main__':
    print(f'{AwesomeNations.nationStates_age()=}')
    print(f'{AwesomeNations.nationStates_birthday()=}')

    print('NATION')
    print(f'{AwesomeNations.Nation().exists()=}')
    print(f'{AwesomeNations.Nation().get_overview()=}')
    print(f'{AwesomeNations.Nation().get_census()=}')

    print('REGION')
    print(f'{AwesomeNations.Region().exists()=}')
    print(f'{AwesomeNations.Region().get_overview()=}')
    print(f'{AwesomeNations.Region().get_world_census(46)=}')
    print(f'{AwesomeNations.Region().get_embassies()=}')