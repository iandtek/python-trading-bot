from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd 
from pprint import pprint 

def gainers(number_of_shares = 300):
    symbols = []
    names = []
    prices = []
    changes = []
    percentChanges = []
    marketCaps = []

    for offset in range(0,number_of_shares,100):
        r = requests.get(f"https://ca.finance.yahoo.com/gainers?offset={offset}&count=100")
        data = r.text
        soup = BeautifulSoup(data, features="lxml")
        for listing in soup.find_all('tr', attrs={'class':'simpTblRow'}):
            for symbol in listing.find_all('td', attrs={'aria-label':'Symbol'}):
                symbols.append(symbol.text)
            for name in listing.find_all('td', attrs={'aria-label':'Name'}):
                names.append(name.text)
            for price in listing.find_all('td', attrs={'aria-label':'Price (Intraday)'}):
                prices.append(float(price.find('span').text.replace(",",".")))
            for change in listing.find_all('td', attrs={'aria-label':'Change'}):
                changes.append(float(change.find('span').text.replace(",",".")))
            for percentChange in listing.find_all('td', attrs={'aria-label':"% Change"}):
                percentChanges.append(float(percentChange.find('span').text.replace("%", "").replace(",",".")))
            for marketCap in listing.find_all('td', attrs={'aria-label':'Market Cap'}):
                marketCapStr = marketCap.find('span').text
                if (marketCapStr[-1] == "M"):
                    marketCaps.append(float(marketCapStr[:-1].replace(",",".")) * 1_000_000)
                elif (marketCapStr[-1] == "B"):
                    marketCaps.append(float(marketCapStr[:-1].replace(",",".")) * 1_000_000_000)
                else:
                    marketCaps.append(0)

    return pd.DataFrame({"symbol": symbols, "name": names, "price": prices, "change": changes, "percentage_change": percentChanges, "market_cap": marketCaps})

def top10():
    return gainers(10)[0:10]

def quote(symbol):
    r = requests.get(f"https://ca.finance.yahoo.com/quote/{symbol}")
    data = r.text
    soup = BeautifulSoup(data, features="lxml")
    return float(soup.find("span", {"class": ["Trsdu(0.3s)", "Fw(b)", "Fz(36px)", "Mb(-4px)", "D(ib)"]}).text)