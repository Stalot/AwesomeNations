from awesomeNations.objects import NationObject

class AwesomeNations:
    class Nation:
        def __init__(self, nation: str = 'testlandia') -> None:
            self.nation = nation

        def exists(self) -> bool:
            nation_name = self.nation
            """
            Checks if nation or region exists by searching for its name.
            """
            exist = NationObject.exists(nation_name)
            return exist
        
        def get_overview(self) -> dict:
            nation_name = self.nation
            """
            Gets an overview of the requested nation.
            """
            overview = NationObject.overview(nation_name)
            return overview

        def get_census(self, censusid: list = [0]) -> dict:
            nation_name = self.nation
            """
            Gets one or more census [0-88] of the requested nation, examples:
            - [0]: Civil rights
            - [46]: Defense Forces
            - [0, 4, 46, 34] ...
            """
            census = NationObject.census(nation_name, censusid)
            return census
    
    def one_plus_one() -> int:
        """
        Extremely important mathematical equation.
        """
        return 1 + 1