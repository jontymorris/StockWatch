# Pro tip: create you own config.py
# by using this as a template

''' ========= LOGIN =========== '''
username = 'your.email@mail.com'
password = 'password123'

''' ======== BUY/SELL ========= '''
buy_amount          = 10    # Dollar amount to buy when a good stock is found.
minimum_stock_price = 1     # The lowest stock price you're willing to buy.
sell_profit_margin  = 2     # Profit percentage to reach before selling a stock.
dividends_bonus     = 2     # Multiplier for stocks with an upcoming dividend (ignored when <=1).

''' ========= TRADING ========= '''
scan_interval   = 30
open_time       = '9:00am'
close_time      = '4:45pm'
days_closed     = ['saturday', 'sunday']
