import json
import os, time
import yfinance as yf
import pandas as pd

class TickerAnalyze(object):
    """"
    classdocs
    """

    staticdir = None
    serverstart = 0

    def __init__(self, staticdir=None, dbhost=None, stkr=None):
        """
        Constructor and initiallizers
        :param staticdir:
        :param dbhost:
        """

        self.staticdir = os.path.join(os.getcwd(), 'ui_www')
        self.serverstart = self.epoch()

    def history(self, ticker=None, period="1mo"):
        """
        :param ticker:
        :return:
        """
        stock = yf.Ticker(ticker)
        print(stock.info)
        hist = stock.history(period="1mo")
        hist = pd.DataFrame(hist)

        return hist

    def market(self, ticker):
        """
        :param ticker:
        :return:
        """
        stock = yf.Ticker(ticker)
        lopt = stock.options[0]
        print("Options: {}".format(lopt))
        opts = stock.option_chain(date=lopt)
        print("Option Length: {}".format(len(opts)))
        for keyrx in opts.calls:
            print(keyrx)
            print(opts[0])

    def info(self, ticker):
        """
        :param ticker:
        :return:
        """
        stock = yf.Ticker(ticker)
        s_info = stock.info
        print("Stock: {}".format(json.dumps(s_info, indent=2)))
        return s_info


    def corelate(self, ticker1, ticker2):
        """
        :param ticker1:
        :param ticker2:
        :return:
        """
        stk1 = self.history(ticker=ticker1)
        stk2 = self.history(ticker=ticker2)


    def epoch(self):
        """
        Returns System Time
        :return:
        """
        epc = int(time.time() * 1000)
        return epc


## main code section
if __name__ == '__main__':
    port = 9005
    www = os.path.join(os.getcwd(), 'ui_www')
    ipaddr = '127.0.0.1'

    tckr = TickerAnalyze()
    #tckr.history(ticker='JNUG', period='1d')

    #tckr.info(ticker='TQQQ')
    #tckr.market(ticker='TQQQ')


    tckr.info(ticker='FNGU')
    tckr.info(ticker='AAPL')
    #tckr.market(ticker='FNGU')