class CensusNotFound(Exception):
    def __init__(self, censusid) -> None:
        self.message = f'Nice try! But censusid={censusid} is out of range. 88 is the maximum - did you forget, or were you hoping I would let it slide? Check your input. I do not do favors.'
        super().__init__(f'{self.message}')

class NationNotFound(Exception):
    def __init__(self, nation_name) -> None:
        self.message = f'Nation "{nation_name}" not found, perhaps this nation no longer exists or never existed.'
        super().__init__(f'{self.message}')

class RegionNotFound(Exception):
    def __init__(self, region_name) -> None:
        self.message = f'Oh no, the region "{region_name}" does not exist. Maybe you forgot a comma? Or did you think programming was easy? Cute.'
        super().__init__(f'{self.message}')

class HTTPError(Exception):
    def __init__(self, status_code) -> None:
        self.message = f'HTTP error, status code: {status_code}. Hope This Totally Pleases-you!'
        super().__init__(f'{self.message}')