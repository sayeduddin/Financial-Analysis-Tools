import pandas as pd
import matplotlib.pyplot as plt

info = pd.read_csv("Stock Screener Data\\screener-stocks.csv")


def analyse(ticker, info):
    df = pd.read_csv(f"Data\\{ticker}.csv")
    # print(df)
    last = df.iloc[-1]
    current = last["Adj Close"]
    ma150 = last["150_ma"]
    ma200 = last["200_ma"]
    ma50 = last["50_ma"]
    annual_low = df["Adj Close"].min()
    annual_high = df["Adj Close"].max()
    monthly_trend = df["200_ma"].iloc[-1] - df["200_ma"].iloc[-21]

    rule1 = current > ma50 > ma150 > ma200
    rule2 = monthly_trend > 0
    rule3 = current > annual_low * 1.3
    rule4 = current > annual_high * 0.75
    rules = rule1 and rule2 and rule3 and rule4

    if rules:
        try:
            row_df = info.loc[(info["Symbol"]) == ticker.replace("-L", "")]
            industry = row_df.iloc[0]["Industry"]
            sector = row_df.iloc[0]["Sector"]
        except:
            try:
                data = pd.read_csv("Data.csv")
                row_df = data.loc[(data["Ticker"]) == ticker.replace("-L", ".L")]
                industry = row_df.iloc[0]["industry"]
                sector = row_df.iloc[0]["sector"]

            except:
                industry = "None"
                sector = "None"

        return [ticker, sector, industry]

    # rule3 = ma50 > ma150
    # print(df.iloc[df["Adj Close"].idxmin()])
    # print(last["Date"])


with open("Tickers.txt", "r") as file:
    tickers = file.readlines()
    tickers = [ticker.strip() for ticker in tickers]
    tickers = [ticker.replace(".L", "-L") for ticker in tickers]

not_found = []
found = []
sectors = {}

for ticker in tickers:
    try:
        stock = analyse(ticker, info)
        if stock:
            found.append(stock)
            if not stock[1] in sectors:
                sectors[stock[1]] = 1
            else:
                sectors[stock[1]] += 1

    except:
        not_found.append(ticker + " information not found")
#print(sectors)

fig = plt.figure()
ax = fig.add_subplot(111)
names = list(sectors.keys())
values = list(sectors.values())

print(names, values)

ax.bar(names, values)
plt.xticks(rotation=45, ha='right')
plt.show()

performance_df = {"Ticker" : [], "Sector" : [], "Industry" : []}
for item in found:
    performance_df["Ticker"].append(item[0])
    performance_df["Sector"].append(item[1])
    performance_df["Industry"].append(item[2])

performance_df = pd.DataFrame(performance_df)
#print([performance_df])

performance_df = performance_df.sort_values(by="Sector")

performance_df.to_csv("Performers.csv" ,index = False)


# print(not_found)
