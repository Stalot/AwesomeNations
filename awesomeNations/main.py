from awesomeNations.objects import NationObject, RegionObject
from datetime import datetime

class AwesomeNations:
    class Nation:
        def __init__(self, nation_name: str = 'testlandia') -> None:
            self.nation_name = nation_name

        def exists(self) -> bool:
            """
            Checks if nation exists by searching for its name.
            """
            exist = NationObject.exists(self)
            return exist
        
        def get_overview(self) -> dict:
            """
            Gets an overview of the requested nation.
            """
            overview = NationObject.overview(self)
            return overview

        def get_census(self, censusid: list = [0]) -> dict:
            """
            Gets one or more census [0-88] of the requested nation, examples:
            - [0]: Civil rights
            - [46]: Defense Forces
            - [0, 4, 46, 34] ...
            """
            census = NationObject.census(self, censusid)
            return census
    class Region:
        def __init__(self, region_name: str = 'The Pacific') -> None:
            self.region_name = region_name
        
        def exists(self) -> bool:
            """
            Checks if region exists by searching for its name.
            """
            exist = RegionObject.exists(self)
            return exist
        
        def get_overview(self) -> dict:
            """
            Gets a overview of the region
            """
            overview = RegionObject.overview(self)
            return overview

    def one_plus_one() -> int:
        """
        Extremely important mathematical equation.
        """
        return 1 + 1
    
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

# Testing to see if my life is worth it:
if __name__ == '__main__':
    print(f'{AwesomeNations.nationStates_age()=}')
    print(f'{AwesomeNations.nationStates_birthday()=}')
    print(f'{AwesomeNations.one_plus_one()=}')

    print('NATION')
    print(f'{AwesomeNations.Nation().exists()=}')
    print(AwesomeNations.Nation().get_overview())
    print(AwesomeNations.Nation().get_census())

    print('REGION')
    print(f'{AwesomeNations.Region().exists()=}')
    print(AwesomeNations.Region().get_overview())