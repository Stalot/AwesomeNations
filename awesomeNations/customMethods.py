from collections.abc import Iterable
from typing import Any, Optional
import time

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

def format_key(string: str, uppercase: bool = False, replace_empty: Optional[str] = None, delete_not_alpha: bool = False) -> str:
    """
    Formats a string.
    """
    formatted_string = string
    if string:
        if delete_not_alpha:
            for char in string:
                if not char.isalpha() and not char.isspace():
                    string = string.replace(char, '')

        if uppercase == False:
            string = string.lower()
        elif uppercase == True:
            string = string.upper()
        else:
            raise ValueError(f"uppercase must be bool or NoneType, not '{type(uppercase).__name__}'.")
                
        if replace_empty:
            string = string.replace(' ', replace_empty)

        formatted_string = string
    return formatted_string

def join_keys(keys: tuple[str, ...] | list[str] = ['hello', 'world'], separator: str = '+') -> str:
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

def get_index(object: tuple | list, index: int, default: Optional[Any] = None) -> Any | None:
    """
    Safely retrieves an element from a tuple or list by index.

    - **object** (tuple | list): The tuple or list from which to retrieve the element.
    - **index** (int): The index of the element to retrieve.
    - **default** (Any, optional): The value to return if the index is out of range. Defaults to None.

    **Returns**: The element at the specified index, or the default value if the index is out of range.
    """
    try:
        return object[index]
    except IndexError:
        return default

def gen_params(dict_data: Optional[dict[str, Any]] = None, join: bool = False, **kwargs: Any) -> Any:
    query = dict_data if dict_data else kwargs
    query_params: dict[str, Any] = {key: str(join_keys(value, "+") if isinstance(value, list) else value).replace(" ", "%20") for key, value in query.items() if value != None}
    #for k, v in query_params.items():
    #    if isinstance(v, list):
    #        query_params[k] = join_keys(v)
    if join:
        parsed_params: list[str] = [f"{k}={v}" for k, v in query_params.items()]
        return join_keys(parsed_params, ";")
    return query_params

if __name__ == "__main__":
    ...