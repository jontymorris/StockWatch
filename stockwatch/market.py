import numpy as np
from stockwatch import util
from datetime import datetime, timedelta
import numpy as np
import config


class Market:

    @staticmethod
    def vwap(df):
        ''' Calculates Volume-weighted average price '''

        q = df.Volume.values
        p = (df.Close.values + df.High.values + df.Low.values) / 3

        if not q.any():
            return df.assign(vwap=p)

        return df.assign(vwap=(p * q).cumsum() / q.cumsum())

    @staticmethod
    def should_buy(market_price, history, margin_percent):
        ''' Decides if the bot should buy or not '''
        
        # ignore zero divide errors
        np.seterr(divide='ignore', invalid='ignore')

        try:
            # calculate vwap
            history = history.groupby(history.index.date, group_keys=False)
            history = history.apply(Market.vwap)

            # calculate direction
            moves = np.gradient(history['vwap'])
            median = np.median(moves)
            average = np.average(moves)

            # calculate margin price
            margin_price = history['vwap'][-1]
            margin_price -= (margin_price * (margin_percent/100))

            # agree if going up and below margin
            if median > 0 and average > 0 and market_price <= margin_price:
                return True

        except Exception as e:
            util.log(f'Warning: {e}')

        return False

    @staticmethod
    def should_sell(original_price, market_price, margin_percent):
        ''' Decides if the bot should sell or not '''
        
        difference = market_price - original_price
        percent_change = (difference / original_price) * 100
        
        # have we reached our profit percentage?
        return percent_change >= margin_percent

    @staticmethod
    def minutes_till_trading():
        ''' Time till NZX is open for trading '''

        now = util.get_nz_time()
        open_dt = datetime.strptime(config.open_time, '%I:%M%p')
        close_dt = datetime.strptime(config.close_time, '%I:%M%p')

        # market is open today
        if now.strftime('%A').lower() not in config.days_closed:

            # open now
            if now.time() >= open_dt.time() and now.time() <= close_dt.time():
                return 0
            
            # hasn't open yet
            if now.time() < open_dt.time():
                return (datetime.combine(now, open_dt.time()) - now).total_seconds()/60
        
        # market has closed
        for i in range(7):
            future = now + timedelta(days=(i+1))
            if future.strftime('%A').lower() not in config.days_closed:
                return (datetime.combine(future, open_dt.time()) - now).total_seconds()/60
 
        util.log("market is never open according to config", error=True)
