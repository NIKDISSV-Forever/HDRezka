"""BeautifulSoup internals"""
from bs4.builder import HTMLTreeBuilder

BUILDER = HTMLTreeBuilder.__subclasses__()[-1]()
