class InvalidQuery(Exception):
    def __init__(self, query, invalid_value) -> None:
        message=f'Invalid value in query: {query}. {type(invalid_value)} {invalid_value}.'
        self.message = message
        super().__init__(f'{self.message}')

class NationException(Exception):
    def __init__(self, nation_name) -> None:
        message = f'Error while searching for this nation, maybe, the nation "{nation_name}" does not exist anymore or never existed.'
        self.message = message
        super().__init__(f'{self.message}')