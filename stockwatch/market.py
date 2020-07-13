from stockwatch import util

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
        try:
            # calculate vwap
            history = history.groupby(history.index.date, group_keys=False)
            history = history.apply(vwap)

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
            util.log('Warning: ' + e)

        return False

    @staticmethod
    def should_sell(original_price, market_price, margin_percent):
        ''' Decides if the bot should sell or not '''
        percent_change = ((market_price - original_price) / original_price) * 100
        return percent_change >= margin_percent

    @staticmethod
    def is_trading_time():
        ''' Checks if NZX is open for trading '''
        #TODO: Change get time till open
        now = util.get_nz_time()

        if now.weekday() < 5:
            if now.hour >= 11 and now.hour <= 15:
                return True
        
        return False
