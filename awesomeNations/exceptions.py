from awesomeNations.customMethods import motivational_quotes, status_code_context

class HTTPError(Exception):
    def __init__(self, status_code) -> None:
        
        self.status_code_context: str | None = status_code_context(status_code)
        if not self.status_code_context:
            self.status_code_context = ""
        else:
            self.status_code_context = f" {self.status_code_context}"

        self.message: str = f'HTTP error, status code: {status_code}{self.status_code_context}. Hope This Totally Pleases-you!'
        super().__init__(f'{self.message}\nJokes aside... {motivational_quotes().capitalize()}')

if __name__ == "__main__":
    raise HTTPError(404)