from awesomeNations.exceptions import NationNotFound, InvalidQuery
from awesomeNations.objects import Nation

class AwesomeNations:
    def __init__(self) -> None:
        pass

    def exists(nation_name: str) -> bool:
        """
        Checks if nation or region exists by searching for its name.
        """
        exist = Nation.check_if_nation_exists(nation_name)
        return exist
    
    def get_overview(nation_name):
        overview = Nation.overview(nation_name)
        return overview
    
    def one_plus_one() -> int:
        return 1 + 1