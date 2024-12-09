class InvalidCensus(Exception):
    def __init__(self, censusid) -> None:
        self.message = f'Census id ({censusid}) is invalid.'
        super().__init__(f'{self.message}')

class NationNotFound(Exception):
    def __init__(self, nation_name) -> None:
        self.message = f'Error while searching for this nation, maybe, the nation "{nation_name}" does not exist anymore or never existed.'
        super().__init__(f'{self.message}')