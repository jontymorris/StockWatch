import sharesies
import yfinance
import numpy as np
from time import sleep
from stockwatch import Market, util
import config


def scan_market(client, buy_amount):
    ''' Scan market to make informed buy/sell decisions '''

    profile = client.get_profile()
    balance = float(profile['user']['wallet_balance'])

    investments = []
    companies = client.get_companies()

    # look to sell stocks
    portfolio = profile['portfolio']

    for company in portfolio:
        fund_id = company['fund_id']
        investments.append(fund_id)

        contribution = float(company['contribution'])
        current_value = float(company['value'])

        # check for a profit
        if Market.should_sell(contribution, current_value, 0.0055):
            code = util.get_code_from_id(fund_id, companies)
            util.log(f'Selling ${current_value} of {code}')
            client.sell(company, float(company['shares']))

    # find new stocks to buy
    for company in companies:

        # check we have balance
        if balance < buy_amount:
            break

        # don't double invest
        if company['id'] in investments:
            continue

        # ignore penny stocks
        price = float(company['market_price'])
        if price < config.minimum_stock_price:
            continue

        symbol = company['code'] + '.NZ'
        stock = yfinance.Ticker(symbol)
        history = stock.history(period='5d', interval='15m')

        # is it a bargain
        if Market.should_buy(price, history, 0.004):
            util.log(f'Buying ${buy_amount} of {symbol}')
            client.buy(company, buy_amount)
            balance -= buy_amount


if __name__ == '__main__':
    # config
    util.log('Loaded config')

    # init client
    client = sharesies.Client()
    if client.login(config.username, config.password):
        util.log('Connected to Sharesies')
    else:
        util.log('Failed to login', error=True)

    # trade loop
    while True:
        if Market.is_trading_time():
            scan_market(client, config.buy_amount)
            util.log('Scanned market')

        sleep(30 * 60)
