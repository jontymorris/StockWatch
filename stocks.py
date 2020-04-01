import json
import sharesies
import yfinance
import numpy as np


def vwap(df):
    q = df.Volume.values
    p = (df.Close.values + df.High.values + df.Low.values) / 3

    if not q.any():
        return df.assign(vwap=p)

    return df.assign(vwap=(p * q).cumsum() / q.cumsum())


def should_buy(market_price, history, margin_percent):
    # calculate vwap
    history = history.groupby(history.index.date, group_keys=False)
    history = history.apply(vwap)

    # calculate direction
    moves = np.gradient(history['vwap'])
    direction = np.average(moves)

    # calculate margin price
    margin_price = history['vwap'][-1]
    margin_price -= (margin_price * margin_percent)

    # agree if going up and below margin
    if direction > 0 and market_price <= margin_price:
        return True

    return False


def should_sell(original_price, market_price, margin_percent):
    percent_change = (market_price - original_price) / original_price
    return percent_change >= margin_percent


stock = yfinance.Ticker('SPK.NZ')
history = stock.history(period='5d', interval='15m')
market_price = stock.info['bid']

if should_buy(market_price, history, 0.005):
    print('We should buy it!')
else:
    print('Nope, not buying this one')

if should_sell(history['Close'][-5], market_price, 0.006):
    print('Sell it now!')
else:
    print('Not selling either')
