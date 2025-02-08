import xmltodict
from pprint import pprint as pp
from awesomeNations.customMethods import format_key, string_is_number

def xml_postprocessor(path, key: str, value):
    key = format_key(key, replace_empty="_", delete_not_alpha=True)
    try:
        formatted_key: str = key
        formatted_value: str = value

        if string_is_number(formatted_value):
            formatted_value: float = float(formatted_value)
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

if __name__ == "__main__":
    myXML = """<NATION id="testlandia">
                    <SECTORS>
                    <BLACKMARKET>0.42</BLACKMARKET>
                    <GOVERNMENT>94.89</GOVERNMENT>
                    <INDUSTRY>3.41</INDUSTRY>
                    <PUBLIC>1.29</PUBLIC>
                    </SECTORS>
                </NATION>
            """
    
    parser = AwesomeParser()
    data = parser.parse_xml(myXML)
    
    pp(data)
    