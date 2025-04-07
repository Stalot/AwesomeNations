from awesomeNations.customMethods import format_key, string_is_number, join_keys
from awesomeNations.exceptions import DataError
from pprint import pprint as pp
from typing import Optional, Literal
import xmltodict
import string
import random

class _ShardsQuery():
    def __init__(self,
                 api_family: tuple[str, str | None],
                 shards: Optional[str | list[str]] = None, 
                 params: Optional[dict[str, str | list[str]]] = None):
        if type(api_family) is not tuple:
            raise ValueError(f"api_family must be tuple or Nonetype, not '{type(api_family).__name__}'")
        
        self.api_family = api_family
        self.query_shards = shards
        self.query_params = params

        if shards:
            if type(shards) is not str:
                self.query_shards = join_keys(shards)

        if params and type(params) is not str:
            for item in params:
                if type(params[item]) is not str:
                    params[item] = join_keys(params[item])
            self.query_params = join_keys([f"{p}={params[p]}" for p in params], ";")

    def querystring(self):
        querystring: str = "?"
        querystring += f"{self.api_family[0]}={self.api_family[1]}&" if self.api_family[0] != "world" else ""
        if self.query_shards:
            querystring += f"q={self.query_shards}"
        else:
            querystring = querystring.replace("&", "")
        if self.query_params:
            querystring += f";{self.query_params}"
        return querystring

class _NationAuth():
    """Nation authentication"""
    def __init__(self,
                 password: Optional[str] = None,
                 autologin: Optional[str] = None):
        if not any((password, autologin)):
            raise ValueError("NationAuth can't be empty, a password or autologin must be given.")
        if password and type(password) is not str:
            raise ValueError(f"password must be str, not {type(password).__name__}")
        if autologin and type(autologin) is not str:
            raise ValueError(f"autologin must be str, not {type(autologin).__name__}")
        self.crip = Criptografy()
        self.password = self.__secret__(password)
        self.autologin = self.__secret__(autologin)
        self.xpin: Optional[int] = None
    
    def __secret__(self, x: str):
        hidden_x = self.crip.encrypt(x) if x else ""
        return hidden_x

    def __show__(self, x: str):
        hidden_x = self.crip.decrypt(x) if x else ""
        return hidden_x
    
    def get(self) -> dict[str]:
        auth_headers: dict[str] = {
            "X-Password": self.__show__(self.password),
            "X-Autologin": self.__show__(self.autologin),
            "X-Pin": self.xpin if self.xpin else ""
        }
        return auth_headers

class AwesomeParser():
    def __init__(self):
        pass
    
    def parse_xml(self, data: dict[str]):
        """
        Parses XML data into a dictionary.
        """
        try:
            parsed_xml: dict = xmltodict.parse(data["data"], data["encoding"], postprocessor=self.xml_postprocessor)
            return parsed_xml
        except Exception as e:
            raise DataError("XML Data", e)

    def xml_postprocessor(self, path, key: str, value: str):
        key = format_key(key, replace_empty="_", delete_not_alpha=True)
        try:
            formatted_key: str = key
            formatted_value: str = value

            if string_is_number(formatted_value):
                formatted_value: complex = complex(formatted_value).real
                formatted_value = int(formatted_value) if formatted_value.is_integer() else formatted_value
            return formatted_key, formatted_value
        except (ValueError, TypeError):
            return key, value

class Criptografy():
    "Basic substitution criptography!"
    def __init__(self):
        self.chars = " " + string.punctuation + string.digits + string.ascii_letters
        self.chars = list(self.chars)
        self.key = self.chars.copy()
        random.shuffle(self.key)
     
     # Encrypt stuff :D
    def encrypt(self, message_to_encrypt: str) -> str:
        plain_text = message_to_encrypt
        cipher_text = ""
        for letter in plain_text:
            index = self.chars.index(letter)
            cipher_text += self.key[index]
        return cipher_text

    # Decrypt stuff :D
    def decrypt(self, message_to_decrypt: str) -> str:
        cipher_text = message_to_decrypt
        plain_text = ""
        for letter in cipher_text:
            index = self.key.index(letter)
            plain_text += self.chars[index]
        return plain_text
    
    def exhaust(self):
        self.key = self.chars.copy()
        random.shuffle(self.key)

if __name__ == "__main__":
    query = _ShardsQuery(("world", None), ("name", "fullname"))
    print(query.querystring())