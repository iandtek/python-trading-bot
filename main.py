import yahoo_finance_scrapper as yf
import trader as trader
import math 
from datetime import datetime
from pprint import pprint
import time

shares = []
cash = 1000
companies_to_invest = 10
money_for_each_company = cash / companies_to_invest

def buy(share):
    global cash
    number_of_shares = math.floor(money_for_each_company / share.price)
    transaction_total = number_of_shares * share.price
    cash -= transaction_total
    if(transaction_total > 0):
        print("Buying " + str(number_of_shares) + " shares of " + share.symbol)
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
    global cash
    print(f"Selling {share} for {current_value} each")
    shares.remove(share)
    cash += current_value * share["amount"]

def sell_shares_with_capital_gain():
    for share in shares[:]:
        current_value = yf.quote(share["symbol"])
        if (current_value > share["price"]):
            sell(share, current_value)

def update_money_for_each_company():
    global money_for_each_company
    money_for_each_company = cash / companies_to_invest

def invest_in_top_10():
    for _ , share in yf.top10().iterrows():
        buy(share)

def main():
    # Start investing in the top 10 gainers
    invest_in_top_10()

    while True:
        update_money_for_each_company()
        sell_shares_with_capital_gain()
        invest_in_top_10()
        pprint(shares)
        print(f"{len(shares)} Shares")
        pv = present_value()
        total = pv + cash
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"Total Cash: {cash} - Portfolio Value: {pv} - Total: {total} - As of {now}")
        time.sleep(5*60)

            
main()