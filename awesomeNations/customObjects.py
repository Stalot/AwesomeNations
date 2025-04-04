from awesomeNations.customMethods import format_key, string_is_number
from awesomeNations.exceptions import DataError
from pprint import pprint as pp
import xmltodict
import string
import random

class AwesomeParser():
    def __init__(self):
        pass
    
    def parse_xml(self, data: dict[str]):
        try:
            parsed_xml: dict = xmltodict.parse(data["data"], data["encoding"], postprocessor=self.xml_postprocessor)
            return parsed_xml
        except Exception as e:
            raise DataError("XML Data Response", e)

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
    criptografy = Criptografy()
    
    msg1 = criptografy.encrypt("Hello!")
    msg2 = criptografy.encrypt("Hello!")
    print(criptografy.decrypt(msg1), msg1)
    print(criptografy.decrypt(msg2), msg2)
    criptografy.exhaust()
    
    msg3 = criptografy.encrypt("Hello!")
    print(criptografy.decrypt(msg3), msg3)