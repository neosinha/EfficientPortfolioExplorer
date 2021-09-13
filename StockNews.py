'''
StockNews.py created by navendusinha
Created on 9/11/21 8:54 PM

This class accomplishes great things
'''

import logging
import os,sys
from pymongo import MongoClient
from stocknews import StockNews




class StockNews(object):
    """
    StockNews.py description
    """
    dtkey = "bec9a6c9c4858f6c333f879727d0f31b"

    def __init__(self, database=None):
        print("Class Initiallized")
        # DB Port Addresses
        self.dbhost = '127.0.0.1'
        self.dbport = 27017

        if database:
            print("Database: {}".format(database))
            dbhostarr = database.split(":")
            self.dbhost = dbhostarr[0]
            if dbhostarr[1]:
                self.dbport = int(dbhostarr[1])

        logging.info("MongoDB Client: {} : {}".format(self.dbhost, self.dbport))
        client = MongoClient(self.dbhost, self.dbport)

        self.dbase = client['c3po']
        self.dbcol = self.dbase['tickernews']

    def newsfeed(self, tckr=None):
        """

        :param tckr:
        :return:
        """
        #tckr = ['AAPL', 'AVGO']
        sn = StockNews(tckr)
        #wt_key=self.dtkey)
        df = sn.summarize()
        print(df)







if __name__ == '__main__':
    print("Hello")
    port = 9009
    staticwww = os.path.join(os.getcwd(), 'ui_www')
    ipaddr = '0.0.0.0'
    dbip = 'data.sinhamobility.com:28018'

    logpath = os.path.join(os.getcwd(), 'log', 'price_stock_table.log')
    logdir = os.path.dirname(logpath)
    os.makedirs(logdir, exist_ok=True)

    cascPath = os.path.abspath(os.getcwd())


    logging.basicConfig(filename=logpath, level=logging.DEBUG, format='%(asctime)s %(message)s')
    handler = logging.StreamHandler(sys.stdout)
    logging.getLogger().addHandler(handler)

    t = StockNews(database=dbip)
    t.newsfeed(tckr=['AAPL', 'C', 'AVGO'])
