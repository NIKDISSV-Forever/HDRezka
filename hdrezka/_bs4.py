from functools import partial

from bs4 import BeautifulSoup, FeatureNotFound

__all__ = ('BeautifulSoup',)
try:
    BeautifulSoup(features='lxml')
    BeautifulSoup = partial(BeautifulSoup, features='lxml')
except FeatureNotFound:
    BeautifulSoup = partial(BeautifulSoup, features='html.parser')
