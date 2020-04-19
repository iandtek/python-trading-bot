import yahoo_finance_scrapper as yf
import trader as trader
import math 
from datetime import datetime
from pprint import pprint

shares = []

cash = 1000
companies_to_invest = 10
money_for_each_company = cash / companies_to_invest

for index, share in yf.top10().iterrows():
    number_of_shares = math.floor(money_for_each_company / share.price)
    transaction_total = number_of_shares * share.price
    cash -= transaction_total
    shares.append({
        'symbol': share.symbol,
        'datetime': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        'transaction_total': transaction_total,
        'amount': number_of_shares,
        'price': share.price
    })

def present_value():
    return trader.present_value(shares) + cash

def sell(share, current_value):
    global cash, shares
    print(f"Selling {share} for {current_value} each")
    shares.remove(share)
    cash += current_value * share["amount"]

for share in shares:
    print(shares)
    current_value = yf.quote(share["symbol"])
    sell(share, current_value)

print(cash)