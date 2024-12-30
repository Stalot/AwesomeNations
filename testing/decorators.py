from awesomeNations.configuration import DEFAULT_HEADERS, DEFAULT_PARSER
from awesomeNations.exceptions import HTTPError
import requests
from bs4 import BeautifulSoup as bs

def validOperation(func):
    def wrapper():
        print('bazinga')
        func()
        pass
    return wrapper

def stuff():
    print('i love tomatoes!')

stuff()