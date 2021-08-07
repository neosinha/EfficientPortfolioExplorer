import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from pandas_datareader import data

# We define the stocks from which we want the data. You should use the ticker name of the stock.
assets = ["AAPL", "MSFT","AMZN","GOOGL","FB","TSLA","V"]

# Define the start date
start = "2016-01-2"
# Today's date
today = datetime.today().strftime('%Y-%m-%d')
# Create an empty dataframe
df_prices = pd.DataFrame()
# Get the  "Adj Close" data from Yahoo Finance
def YahooData(dataframe,assets_list,start_date,end_date):
    for i in assets_list:
        dataframe[i] = data.DataReader(i,data_source='yahoo',start=start_date , end=end_date)["Adj Close"]
    return dataframe

df = YahooData(df_prices,assets,start,today)

# We transform the data to it´s logarithmic returns
df = np.log(df).diff()
# Drop the first row because we loose information we the logarithmic return.
df = df.dropna()

# Compute the Expected Returns, we multiply daily return by 252 because there are 252 business days in the US.
def expected_return(dataframe):
    expected_returns = []
    for i in df.columns:
        expected_returns.append(df[i].mean()*252)
    return np.array(expected_returns)

returns = expected_return(df)


# Covariance Matrix, we multiply it by 252 to make it annual, this is need for the expected returns
df_cov = df.cov()*252
# Correlation Matrix
df_corr = df.corr()

# Inverse matrix of the variance-covariance matrix:
df_cov_inv = pd.DataFrame(np.linalg.pinv(df_cov.values), df_cov.columns, df_cov.index)

# Plotting of the correlation matrix:
correlation_mat = df.corr()
def plot_corr_matrix(corr_matrix):
    plt.figure(figsize=(12.2,4.5))
    sns.heatmap(correlation_mat, annot = True)
    plt.title('Correlation Matrix',fontsize=18)
    plt.xlabel('Stocks',fontsize=14)
    plt.ylabel('Stocks',fontsize=14)
    plt.show()

print(correlation_mat)
print("==================================")
print(df_cov)

#plot_corr_matrix(correlation_mat)
# Simulating 5000 portfolios
num_port = 5000
# Creating an empty array to store portfolio weights
all_wts = np.zeros((num_port, len(df.columns)))
# Creating an empty array to store portfolio returns
port_returns = np.zeros((num_port))
# Creating an empty array to store portfolio risks
port_risk = np.zeros((num_port))
# Creating an empty array to store portfolio sharpe ratio
sharpe_ratio = np.zeros((num_port))

for i in range(num_port):
    wts = np.random.uniform(size = len(price_data.columns))
    wts = wts/np.sum(wts)

    # saving weights in the array

    all_wts[i,:] = wts

    # Portfolio Returns

    port_ret = np.sum(log_ret.mean() * wts)
    port_ret = (port_ret + 1) ** 252 - 1

    # Saving Portfolio returns

    port_returns[i] = port_ret


    # Portfolio Risk

    port_sd = np.sqrt(np.dot(wts.T, np.dot(cov_mat, wts)))

    port_risk[i] = port_sd

    # Portfolio Sharpe Ratio
    # Assuming 0% Risk Free Rate

    sr = port_ret / port_sd
    sharpe_ratio[i] = sr