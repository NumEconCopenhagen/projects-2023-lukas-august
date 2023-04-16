# Import numpy, pandas, datetime and matplotlib
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

# Import Yahoo Finance API
import yfinance as yf
yf.pdr_override()
from pandas_datareader import data as pdr


# Function used to retreive data from Yahoo Finance through the API for specified stock (ticker) and date interval
def GetStockData(ticker,start,end):

    # Creating a data from with stock data for the ticker and date interval
    df = pdr.get_data_yahoo(ticker, start=start, end=end)

    # Return datafrome
    return df

# Function used for getting data from multiple tickers (defined in list)
def GetMultipleStock(tickers):

    # Creating an empty dataframe
    stockdata = pd.DataFrame()

    # Iterate over list of tickers (argument)
    for i in tickers:

        # Calling the GetStockData function to retreive data through the API
        df = GetStockData(i,start_date,end_date)

        # Transforming the data: Keeping the adjusted closing price and renaming it the ticker name, and dropping the other data points.
        df.rename(columns = {'Adj Close': i}, inplace = True)
        df.drop(['Open','High','Low','Close','Volume'], axis=1, inplace = True)

        # Joining the data for the specific ticker in a combined dataframe
        if stockdata.empty:
            stockdata = df
        else:
            stockdata = stockdata.join(df, how='outer')

        # Drop rows containing NaN values
        stockdata.dropna(inplace = True)

    # Return the combined dataframe containing the pice data for the list of tickers
    return stockdata


# Specify tickers and stat and end dates
tickers = ['AAPL','META','PFE','NVO','CS','DANSKE.CO']

# Start and end date used to define the date interval when calling the API
start_date = '2020-1-1'
end_date = '2023-3-1'

# Call function to receive stockprices
data = GetMultipleStock(tickers)

# Styling the plots globally
style = 'Solarize_Light2'
plt.style.use(style)

# Calculating the dayly returns
dayly_returns = data.pct_change()

# Indexing the price data and adding a rolling average (200 days)
index_plot = data.apply(lambda x: x / x[0])
index_plot_moving = index_plot.rolling(200).mean()

# Plotting the indexed price data as well as the rolling average in the same graph
ax = index_plot.plot(linewidth = 0.9, color=['#FF26AE', '#A210E6', '#8871FA', '#1E62E6', '#50DFFA', '#FF5144'], xlabel='')
index_plot_moving.plot(ax=ax, linestyle = '--', linewidth = 0.7, legend=None,color=['#FF26AE', '#A210E6', '#8871FA', '#1E62E6', '#50DFFA', '#FF5144'], xlabel='')
plt.show()

# Plotting the dayly returns for each ticker i seperate histograms but in the same figure, using subplots
for i, col in enumerate(tickers):
    plt.subplot(2, 3, i + 1)
    plt.hist(dayly_returns[col], range=[-0.1, 0.1], density=True, bins='auto')
    plt.title(col, fontsize = 9)
plt.tight_layout()
plt.show()

# Calculating the correlation between each ticker
data_corr = data.corr()

# Plot the correlations in a matrix
data_heat = data_corr.values
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
heatmap = ax.pcolor(data_heat, cmap = plt.cm.RdYlGn)
fig.colorbar(heatmap)
ax.set_xticks(np.arange(data_heat.shape[0]) + 0.5, minor = False)
ax.set_yticks(np.arange(data_heat.shape[1]) + 0.5, minor = False)
ax.invert_yaxis()
ax.xaxis.tick_top()
column_labels = data_corr.columns
row_labels = data_corr.index
ax.set_xticklabels(column_labels)
ax.set_yticklabels(row_labels)
plt.xticks(rotation = 90)
heatmap.set_clim(-1, 1)
plt.tight_layout()
plt.style.use(style)
plt.show()
