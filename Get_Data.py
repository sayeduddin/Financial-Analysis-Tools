import json as j
import time as t
import pandas as pd
import requests as r
import datetime as dt


def time_to_date(time):
    return str(time[0]) + "-" + (1 - time[1]//10) * "0" + str(time[1]) + "-" + (1 - time[2]//10) * "0" + str(time[2])


def get_df(ticker):
    now = int(t.mktime(dt.datetime.now().timetuple()))

    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?symbol={ticker}&period1={now - 24*3600*365}&period2={now}&useYfid=true&interval=1d"
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

    #avg_volume = df.iloc[-20:]["Volume"].mean()
    #print(avg_volume)

    return df


with open("Tickers.txt", "r") as file:
    tickers = file.readlines()
    tickers = [ticker.strip() for ticker in tickers]


#for ticker in tickers[:10]:
#    print(get_df(ticker))

#tickers = ["BGSC.L", "GPOR.L", "JEO.L"]

for ticker in tickers:
    dash = ticker.replace(".L", "-L")
    #print(dash)
    try:
        get_df(ticker).to_csv(f"C:\\Users\\Sayed\\Desktop\\Python For Finance\\Trend Template\\Fast\\Data\\{dash}.csv", index = False)
    except:
        print(ticker)
