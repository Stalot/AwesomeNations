import xmltodict
from pprint import pprint as pp
from awesomeNations.customMethods import format_key, string_is_number
from typing import Optional

def xml_postprocessor(path, key: str, value: str):
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

class AwesomeParser():
    def __init__(self):
        pass
    
    def parse_xml(self, xml: str):
        parsed_xml: dict = xmltodict.parse(xml, postprocessor=xml_postprocessor)
        return parsed_xml

class Authentication():
    def __init__(self, password: Optional[str] = None, autologin: Optional[str] = None):
        self.password = password
        self.autologin = autologin
    
    def get(self) -> dict[str]:
        auth_headers: dict[str] = {
            "X-Password": self.password if self.password else "",
            "X-Autologin": self.autologin if self.autologin else ""
        }
        return auth_headers

if __name__ == "__main__":
    myXML = """
<NATION id="unirstate">
    <CENSUS>
        <SCALE id="76">
            <SCORE>2.386847e+15</SCORE>
            <RANK>11169</RANK>
            <RRANK>1</RRANK>
        </SCALE>
    </CENSUS>
</NATION>
"""
    
    parser = AwesomeParser()
    data = parser.parse_xml(myXML)
    
    pp(data)
    