import time
from collections.abc import Iterable

def string_is_number(string: str) -> bool:
    """
    Checks if string is a number or not.
    """
    if type(string) != str:
        raise TypeError(f"{type(string).__name__} {string} is not a string.")
    try:
        complex(string)
        return True
    except ValueError:
        return False

def format_key(string: str = None, uppercase: bool = False, replace_empty: str = None, delete_not_alpha: bool = False) -> str:
    """
    Formats a string.
    """
    formatted_string = None
    if string:
        if delete_not_alpha:
            for char in string:
                if not char.isalpha() and not char.isspace():
                    string = string.replace(char, '')

        if not uppercase:
            string = string.lower()
        else:
            string = string.upper()

        if replace_empty:
            string = string.replace(' ', replace_empty)

        formatted_string = string
    return formatted_string

def join_keys(keys: list[str] | tuple[str] = ['hello', 'world'], separator: str = '+') -> str:
    """
    Joins multiple string keys in a single string.
    """
    result = keys
    if isinstance(keys, Iterable) and type(keys) is not str:
        string_keys = (str(key) for key in keys)
        result = separator.join(string_keys)
    return str(result)

def generate_epoch_timestamp() -> int:
    timestamp: int = int(time.time())
    return timestamp

if __name__ == "__main__":
    myList = 46
    result = join_keys(myList)
    print(f"{result} = {type(result)}")