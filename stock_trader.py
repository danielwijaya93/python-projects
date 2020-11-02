import yfinance as yf
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("fivethirtyeight")

def stock_algo(stock, start, end, short_sma, long_sma):
    df = yf.download(stock,start, end, interval='1d')
    
    SMAs=[short_sma, long_sma]
    for i in SMAs:
        df["SMA_"+str(i)]= df.iloc[:,4].rolling(window=i).mean()
    
    trends = []
    
    for i in df.index:
        SMA_short=df["SMA_"+str(short_sma)]
        SMA_long =df["SMA_"+str(long_sma)]
        close=df['Adj Close'][i]

        if(SMA_short[i] > SMA_long[i]):
            trend = 'up'
            trends.append(trend)
        else:
            trend = 'down'
            trends.append(trend)

    df["trends"] = trends

    df["prev_trend"] = df.trends.shift(1)
    
    flags = []
    for i in df.index:
        trends = df["trends"]
        prev_trend = df["prev_trend"]

        if (trends[i] != prev_trend[i]):
            flag = 'change'
            flags.append(flag)
        else:
            flag = 'same'
            flags.append(flag)

    df["flags"] = flags
    
    buy_price = []
    sell_price = []

    for i in df.index:
        t = df["trends"]
        f = df["flags"]
        close = df["Adj Close"]

        if (t[i] == "up" and f[i] == "change"):
            buy_price.append(close[i])
            sell_price.append(np.nan)
        elif (f[i] == "same"):
            buy_price.append(np.nan)
            sell_price.append(np.nan)
        else:
            buy_price.append(np.nan)
            sell_price.append(close[i])

    df["Buy Price"] = buy_price
    df["Sell Price"] = sell_price
    
    df = df.drop(columns=["Open", "High", "Low", "Close", "Volume", "trends", "prev_trend", "flags"])
    
    return df

stock = 'AAPL'
start = '2016-01-01'
end = dt.datetime.now()
short_sma = 20
long_sma = 50

df = stock_algo(stock,start,end, short_sma, long_sma)

df.head()

plt.figure(figsize=(12.6, 4.6))
plt.plot(df["Adj Close"], label = "AAPL", alpha = 0.35)
plt.plot(df["SMA_20"], label = "SMA_20", alpha = 0.35)
plt.plot(df["SMA_50"], label = "SMA_50", alpha = 0.35)
plt.scatter(df.index, df["Buy Price"], label = "Buy", marker = "^", color = "green")
plt.scatter(df.index, df["Sell Price"], label = "Sell", marker = "v", color = "red")
plt.title("Apple Adj Close Price Buy & Sell Signals")
plt.xlabel("2016 - YTD")
plt.ylabel("Adj Close Price USD")
plt.legend(loc = "upper left")
plt.savefig("apple.png")
