from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import pandas as pd
import pickle
import threading
import sys


class StockNews(object):
    """
    StockNews.py description
    """
    dtkey = "bec9a6c9c4858f6c333f879727d0f31b"

    def __init__(self, database=None):
        print("Class Initiallized")
        # DB Port Addresses
        self.dbhost = '127.0.0.1'


if __name__ == '__main__':
    #Example Usage
    fomc = FOMC()
    df = fomc.get_statements()
    fomc.pickle("./df_minutes.pickle")