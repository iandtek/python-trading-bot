import yahoo_finance_scrapper as yf

def present_value(shares):
    total = 0
    for share in shares:
        total += yf.quote(share["symbol"]) * share["amount"]
    return total
