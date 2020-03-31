import json
from sharesies import Sharesies


with open('config.json', 'r') as handle:
    config = json.loads(handle)

client = Sharesies()
client.login(config['Username'], config['Password'])

companies = client.get_companies()

# Company: 'code', 'market_price', 'name'

# Sharesies return daily prices.
# I need more data...
