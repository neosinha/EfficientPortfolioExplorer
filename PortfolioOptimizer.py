from pandas_datareader import data as yfindata
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns


import argparse
import ast
import json
import logging
import os
import sys
import threading
import time

import cherrypy as HttpServer
import paho.mqtt.client as mqtt
from pymongo import MongoClient
from typing import Any


class POptmizer(object):

    def __init__(self, staticdir=None, database=None, logexport=None):
        """

        :param staticdir:
        :param database:
        :param logexport:
        """

        self.staticdir = os.path.join(os.getcwd(), 'ui_www')
        if staticdir:
            self.staticdir = staticdir

        #Intializing the upload directory
        uploaddir = os.path.join(self.staticdir, '..', 'uploads')
        if uploaddir:
            self.uploaddir = uploaddir

    @HttpServer.expose()
    def index(self):
        """
        Returns the root of the web-application
        :return:
        """
        return open(os.path.join(self.staticdir, "index.html"))


    @HttpServer.expose()
    def getstocktable(self, assetdata=None):
        """
        Gets the stock tickers from frontend and loads the data-frames
        :param assetdata:
        :return:
        """
        robj = {}
        if assetdata:
            assetdata = json.loads(assetdata)
            logging.info("Ticker Requested: {}".format(assetdata))

            assetweights = assetdata['assets']
            startdate = assetdata['startdate']
            assets = []
            weights = []
            for awel in assetweights:
                assetel, weightel = awel.split("=")
                assets.append(assetel.upper())
                weights.append(float(weightel)/100)
                print("Asset: {}/Weight: {}".format(assetel, weightel))


            px = PortfolioMaker(assets=assets,
                                weights=weights,
                                staticdir=os.path.join(self.staticdir, 'images', 'assetperformance'))

            assetp = px.loadstocks(priceType='Adj Close')
            correlobj = px.covariancetable()
            returns = px.portfolioreturns()
            sharperatio= px.sharpeRatio()
            efficientFront = px.efficientPortfolio()

            robj['asset'] = assetp
            robj['covariancetable'] = correlobj
            robj['returns'] = returns
            robj['shareratio'] = sharperatio


        print(json.dumps(robj, indent=2))
        return json.dumps(robj)



class PortfolioMaker(object):

    _assets  = []
    _stardate =  None
    _enddate =  None

    _weights = None
    _pd = None
    _df = None

    def __init__(self, assets, startdate=None, enddate=None, weights=None, staticdir=None):
        """

        :param assets:
        :param startdate:
        """
        self._assets = assets
        print("Assets: {}".format(assets))
        yy = (datetime.now().year)-10
        mm = datetime.now().month
        dd = datetime.now().day

        print("Date: {}-{}-{}".format(yy, mm, dd))

        self._stardate = '{}-{}-{}'.format(yy, mm, dd)
        if startdate:
            self._stardate = startdate

        self._enddate = datetime.today().strftime('%Y-%m-%d')

        if enddate:
            self._enddate = enddate

        self._weights = weights

        #Directory for generating chart images
        self._staticdir = os.path.join(os.getcwd(), 'ui_www', 'images')
        if staticdir:
            self._staticdir = staticdir

        os.makedirs(staticdir, exist_ok=True)


    def loadstocks(self, priceType=None):
        self._df = pd.DataFrame()
        #Store the adjusted close price of stock into the data frame
        priceIdx = 'Adj Close'
        if priceType:
            priceIdx = priceType

        for stock in self._assets:
            print('Asset: {}, {}, {}'.format(stock, self._stardate, self._enddate))
            self._df[stock] = yfindata.DataReader(stock, data_source='yahoo',
                                            start=self._stardate,
                                            end=self._enddate)['Adj Close']


        title = 'Portfolio Adj. Close Price History'
        #Create and plot the graph
        # 4:3
        plt.figure(figsize=(12,9)) #width = 12.2in, height = 4.5

        # Loop through each stock and plot the Adj Close for each day
        for c in self._df.columns.values:
            plt.plot( self._df[c],  label=c)
            #plt.plot( X-Axis , Y-Axis, line_width, alpha_for_blending,  label)

        plt.title(title)
        plt.xlabel('Date',fontsize=18)
        plt.ylabel('Adj. Price USD ($)',fontsize=18)
        plt.legend(self._df.columns.values, loc='upper left')

        #plt.show()
        assetpath = os.path.join(self._staticdir, 'portfolio-{}.png'.format(int(datetime.now().timestamp())) )
        #print(datetime.now().timestamp())

        print("AssetPath: {}".format(assetpath))
        plt.savefig(assetpath, transparent=True)



        #robj = self._df.to_dict(orient='records')
        #print(robj)
        return os.path.basename(assetpath)

    def covariancetable(self):
        """
        Generate and Make Covariance Table
        :return:
        """
        #Show the daily simple returns, NOTE: Formula = new_price/old_price - 1
        robj = {}

        self.returns = self._df.pct_change()
        self.cov_matrix_annual = self.returns.cov() * 252
        self.corel_matrix = self.returns.corr()

        #port_variance = np.dot(self._weights.T, np.dot(cov_matrix_annual, self._weights))
        #port_volatility = np.sqrt(port_variance)
        #print(cov_matrix_annual)
        #print("=====")
        #print(corel_matrix)

        plt.figure(figsize=(12, 9))
        sns.heatmap(self.corel_matrix, annot = True)
        plt.title('Correlation Matrix',fontsize=18)
        plt.xlabel('Stocks',fontsize=14)
        plt.ylabel('Stocks',fontsize=14)
        assetpath = os.path.join(self._staticdir, 'covariance-{}.png'.format(int(datetime.now().timestamp())) )
        #print(datetime.now().timestamp())
        print("AssetPath: {}".format(assetpath))
        plt.savefig(assetpath, transparent=True)

        robj['correlation'] = os.path.basename(assetpath)
        robj['cor'] = self.corel_matrix.to_dict(orient='records')
        robj['cov'] = self.cov_matrix_annual.to_dict(orient='records')

        returns_frame = pd.concat([self._df, self.returns])
        print(returns_frame.describe())
        xlfile = os.path.join(self._staticdir, 'portfolio-{}.xlsx'.format(int(datetime.now().timestamp())))  # type:

        robj['msexcel'] = os.path.basename(xlfile)

        with pd.ExcelWriter(xlfile) as writer:
            returns_frame.to_excel(writer,sheet_name='AdjustedClose')
            self.returns.to_excel(writer,sheet_name='Returns')
            self.corel_matrix.to_excel(writer, sheet_name="CorelMat")
            self.corel_matrix.to_excel(writer, sheet_name="CorelMat")
            self.cov_matrix_annual.to_excel(writer, sheet_name="CovriancelMat")

        return robj

    def portfolioreturns(self):
        """
        Perform calculations for expected returns and volatilty
        :return:
        """
        # Assign weights to the stocks. Weights must = 1 so 0.2 for each
        weights = np.array(self._weights)

        port_variance = np.dot(weights.T, np.dot(self.cov_matrix_annual, weights))
        port_volatility = np.sqrt(port_variance)

        portfolioSimpleAnnualReturn = np.sum(self.returns.mean()*weights) * 252
        percent_var = str(round(port_variance, 2) * 100)
        percent_vols = str(round(port_volatility, 2) * 100)
        percent_ret = str(round(portfolioSimpleAnnualReturn, 2)*100)

        print("Expected annual return : {}%".format(percent_ret))
        print('Annual volatility/standard deviation/risk : {}'.format(percent_vols))
        print('Annual variance : {}'.format(percent_var))

        robj = {'return' : percent_ret, 'volatility': percent_vols, 'variance': percent_var}

        return robj

    def sharpeRatio(self):
        """
        Analyze stats for Efficient Frontier
        :return:
        """
        mu = expected_returns.mean_historical_return(self._df)#returns.mean() * 252
        S = risk_models.sample_cov(self._df) #Get the sample covariance matrix
        ef = EfficientFrontier(mu, S)

        sharpe_weights = ef.max_sharpe() #Maximize the Sharpe ratio, and get the raw weights
        cleaned_weights = ef.clean_weights()
        print(cleaned_weights) #Note the weights may have some rounding error, meaning they may not add up exactly to 1 but should be close
        sharpe_pf = ef.portfolio_performance(verbose=True)
        print("Sharpe: {}".format(sharpe_pf))

        from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
        latest_prices = get_latest_prices(self._df)
        weights = cleaned_weights
        da = DiscreteAllocation(weights, latest_prices, total_portfolio_value=10000)
        allocation, leftover = da.lp_portfolio()

        robj = {'allocation': str(allocation), 'leftover': str(leftover),
                'weights': weights, 'sharpe':  sharpe_weights }

        return robj


    def rand_weights(self, n):
        ''' Produces n random weights that sum to 1 '''
        weights = np.random.rand(n)
        weights /= np.sum(weights)

        return weights


    def efficientPortfolio(self):
        """

        :return:
        """
        # Create a random portfolio distribution weigths, that sums 100%
        print(self.rand_weights(len(self._assets)))

        pfolio_returns = []
        pfolio_volatilities = []
        pfolio_wts = pd.DataFrame(columns=self._assets)

        porfoliosize = 1000*len(self._assets)
        for x in range(porfoliosize):
            weights = self.rand_weights(len(self._assets))
            pfolio_returns.append(np.sum(weights * self.returns.mean()) * 252)
            pfolio_volatilities.append(np.sqrt(np.dot(weights.T,np.dot(self.cov_matrix_annual * 252, weights))))
            #pfolio_wts.append(weights)
            pfolio_wts.append(pd.DataFrame(weights))

        pfolio_returns = np.array(pfolio_returns)
        pfolio_volatilities = np.array(pfolio_volatilities)

        #print("E(Rp): {}".format(pfolio_returns))
        #print("Sigma(p): {}".format(pfolio_volatilities))

        portfolios = pd.DataFrame({'Volatility': pfolio_volatilities, 'Return': pfolio_returns})
        #portfolios.plot(x='Volatility', y='Return', kind='scatter', figsize=(10, 6));
        #plt.scatter(results[0, :], results[1, :], c=results[2, :], cmap='YlGnBu', marker='o', s=10, alpha=0.3)
        plt.figure(figsize=(12, 9))
        colors = np.random.randint(100, size=(porfoliosize))
        plt.scatter(pfolio_volatilities, pfolio_returns, c=colors, cmap='YlGnBu', alpha=0.3,  marker='o', s=3)
        #plt.scatter()
        plt.xlabel('Expected Volatility')
        plt.ylabel('Expected Return')

        assetpath = os.path.join(self._staticdir, 'eportfolio-{}.png'.format(int(datetime.now().timestamp())) )

        print("AssetPath: {}".format(assetpath))
        plt.savefig(assetpath, transparent=True)




# main code section
if __name__ == '__main__':
    port = 9009
    www = os.path.join(os.getcwd(), 'ui_www')
    ipaddr = '0.0.0.0'
    dbip = 'data.sinhamobility.com:28018'

    logpath = os.path.join(os.getcwd(), 'log', 'efficientoptimzer.log')
    logdir = os.path.dirname(logpath)
    os.makedirs(logdir, exist_ok=True)

    cascPath = os.path.abspath(os.getcwd())

    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--port", required=False, default=9005,
                    help="Port number to start HTTPServer." )

    ap.add_argument("-i", "--ipaddress", required=False, default='127.0.0.1',
                    help="IP Address to start HTTPServer")

    ap.add_argument("-d", "--dbaddress", required=False, default=dbip,
                    help="Database Address to start HTTPServer")

    ap.add_argument("-s", "--static", required=False, default=www,
                    help="Static directory where WWW files are present")

    ap.add_argument("-c", "--cascpath", required=False, default=cascPath,
                    help="Directory where cascase files are found, defaults to %s" % (cascPath))

    ap.add_argument("-f", "--logfile", required=False, default=logpath,
                    help="Directory where application logs shall be stored, defaults to %s" % (logpath) )


    # Parse Arguments
    logexport = os.getcwd()

    args = vars(ap.parse_args())
    if args['port']:
        portnum = int(args["port"])

    if args['ipaddress']:
        ipadd = args["ipaddress"]

    if args['dbaddress']:
        dbip= args["dbaddress"]

    if args['static']:
        staticwww = os.path.abspath(args['static'])

    if args['logfile']:
        logpath = os.path.abspath(args['logfile'])
    else:
        if not os.path.exists(logdir):
            print("Log directory does not exist, creating %s" % (logdir))
            os.makedirs(logdir)

    if args['cascpath']:
        cascPath = args['cascpath']

    logging.basicConfig(filename=logpath, level=logging.DEBUG, format='%(asctime)s %(message)s')
    handler = logging.StreamHandler(sys.stdout)
    logging.getLogger().addHandler(handler)

    HttpServer.config.update({'server.socket_host': ipadd,
                              'server.socket_port': portnum,
                              'server.socket_timeout': 60,
                              'server.thread_pool': 8,
                              'server.max_request_body_size': 0
                              })

    logging.info("Static dir: %s " % (staticwww))
    conf = { '/': {
        'tools.sessions.on': True,
        'tools.staticdir.on': True,
        'tools.staticdir.dir': staticwww}
    }

    HttpServer.quickstart(POptmizer(staticdir=staticwww,
                                     database=dbip, logexport=logexport,
                                    ),
                          '/', conf)


