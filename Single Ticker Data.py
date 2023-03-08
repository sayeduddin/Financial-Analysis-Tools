import json as j
import time as t
import pandas as pd
import requests as r
import datetime as dt
import pandas_ta as pt


def time_to_date(time):
    return str(time[0]) + "-" + (1 - time[1]//10) * "0" + str(time[1]) + "-" + (1 - time[2]//10) * "0" + str(time[2])


def get_df(ticker):
    now = int(t.mktime(dt.datetime.now().timetuple()))

    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?symbol={ticker}&period1={now - 24*3600*2000}&period2={now}&useYfid=true&interval=1d"
    print(url)
    json_data = r.get(url, headers = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}).text
    data = j.loads(json_data)

    timestamps = data["chart"]["result"][0]["timestamp"]
    dates = [time_to_date(t.localtime(time)) for time in timestamps]
    adjclose = data["chart"]["result"][0]["indicators"]["adjclose"][0]["adjclose"]
    open = data["chart"]["result"][0]["indicators"]["quote"][0]["open"]
    close = data["chart"]["result"][0]["indicators"]["quote"][0]["close"]
    high = data["chart"]["result"][0]["indicators"]["quote"][0]["high"]
    low = data["chart"]["result"][0]["indicators"]["quote"][0]["low"]
    volume = data["chart"]["result"][0]["indicators"]["quote"][0]["volume"]

    df = pd.DataFrame({"Date" : dates, "Open" : open, "Close" : close, "High" : high, "Low" : low, "Adj Close" : adjclose, "Volume" : volume})

    ma_list = [20, 50, 150, 200]
    for ma in ma_list:
        df[str(ma)+"_ma"] = df["Adj Close"].rolling(window = ma).mean()

    df["% Change"]=df["Adj Close"].pct_change()
    df["rsi"]=pt.rsi(df["Adj Close"])

    return df


ticker=input("Ticker:").upper()


try:
    get_df(ticker).to_csv(f"C:\\Users\\Sayed\\Desktop\\Python For Finance\\Trend Template\\Fast\\Data\\{ticker}.csv", index = False)
    print(f"{ticker} has been updated.")
except:
    print("An error has occured")

input()

