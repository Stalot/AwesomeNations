from awesomeNations.baseExceptions import NSConnectionError
from typing import Optional


def status_code_context(status_code: int) -> Optional[str]:
    common_status_codes: dict = {
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        408: "Request Timeout",
        409: "Conflict",
        429: "Too Many Requests",
        500: "Internal Server Error",
        502: "Bad Gateway",
        503: "Service Unavailable",
        504: "Gateway Timeout",
    }

    output: Optional[str] = common_status_codes.get(status_code)
    return output


class HTTPError(NSConnectionError):
    """
    Exception raised when request status code is not `200` (Failed).
    """
    def __init__(self, status_code) -> None:
        context: Optional[str] = status_code_context(status_code)
        if not context:
            context = ""
        else:
            context = f" {context}"

        msg: str = f'HTTP error, status code: {status_code}{context}'
        super().__init__(f'{msg}. Hope This Totally Pleases-you!')


class NSConnectionUnreachable(NSConnectionError):
    def __init__(self, reason: str) -> None:
        msg = f"An error occuried while estabishing connection: '{reason}'"
        super().__init__(f"{msg}.\nMaybe it's a problem with your internet?")


class DataError(UnicodeError):
    """
    Exception to warn about data processing failures, such
    encoding or decoding errors.
    """
    def __init__(self, data_name: str, reason: str):
        message = f"Could not process [{data_name}]: {reason}"
        super().__init__(message)


if __name__ == "__main__":
    try:
        raise DataError('XML', 'XML is cringe, json is cooler!')
    except UnicodeError as e:
        print(e)