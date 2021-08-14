import numpy as np
import pandas as pd
from pandas_datareader import data as wb
from pandas_datareader import data as yfindata

import matplotlib.pyplot as plt
from datetime import datetime
import os




class MarkowitzOptimizer(object):

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
        self._enddate = datetime.today().strftime('%Y-%m-%d')


    def rand_weights(self, n):
        ''' Produces n random weights that sum to 1 '''
        weights = np.random.rand(n)
        weights /= np.sum(weights)

        return weights

    def datahauler(self):
        """

        :return:
        """
        assets = self._assets
        self.bvmf_data = pd.DataFrame()
        for stock in assets:
            print('Asset: {}, {}, {}'.format(stock, self._stardate, self._enddate))
            self.bvmf_data[stock] = yfindata.DataReader(stock, data_source='yahoo',
                                               start=self._stardate,
                                               end=self._enddate)['Adj Close']

        self._log_returns = np.log(self.bvmf_data / self.bvmf_data.shift(1))

    def optimizer(self):

        # Create a random portfolio distribution weigths, that sums 100%
        print(self.rand_weights(len(self._assets)))

        pfolio_returns = []
        pfolio_volatilities = []
        pfolio_wts = pd.DataFrame(columns=self._assets)

        porfoliosize = 1000*len(self._assets)
        for x in range(porfoliosize):
            weights = self.rand_weights(len(self._assets))
            pfolio_returns.append(np.sum(weights * self._log_returns.mean()) * 252)
            pfolio_volatilities.append(np.sqrt(np.dot(weights.T,np.dot(self._log_returns.cov() * 252, weights))))
            #pfolio_wts.append(weights)
            pfolio_wts.append(pd.DataFrame(weights))

        pfolio_returns = np.array(pfolio_returns)
        pfolio_volatilities = np.array(pfolio_volatilities)

        #print("E(Rp): {}".format(pfolio_returns))
        #print("Sigma(p): {}".format(pfolio_volatilities))

        portfolios = pd.DataFrame({'Volatility': pfolio_volatilities, 'Return': pfolio_returns})
        #portfolios.plot(x='Volatility', y='Return', kind='scatter', figsize=(10, 6));
        #plt.scatter(results[0, :], results[1, :], c=results[2, :], cmap='YlGnBu', marker='o', s=10, alpha=0.3)
        colors = np.random.randint(100, size=(porfoliosize))
        plt.scatter(pfolio_volatilities, pfolio_returns, c=colors, cmap='viridis', alpha=0.3,  marker='o', s=3)
        plt.xlabel('Expected Volatility')
        plt.ylabel('Expected Return')

        xlfile = os.path.join(os.getcwd(), 'portfolio-{}.xlsx'.format(int(datetime.now().timestamp())))  # type:
        with pd.ExcelWriter(xlfile) as writer:
            self.bvmf_data.to_excel(writer,sheet_name='AdjustedClose')
            portfolios.to_excel(writer, sheet_name="Portfolio")

        plt.show()

# main code section
if __name__ == '__main__':
    port = 9009
    www = os.path.join(os.getcwd(), 'ui_www')

    mkw = MarkowitzOptimizer(assets=['AAPL', 'SPY', 'BLV'])
    mkw.datahauler()
    mkw.optimizer()


