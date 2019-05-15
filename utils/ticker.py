import requests

TICKER_ADDRESS = "https://api.coinmarketcap.com/v1/ticker/"

def get_ticker(currency):
    ticker_address = TICKER_ADDRESS + currency + "/"
    resp = requests.get(ticker_address)
    price_usd = resp.json()[0]['price_usd']
    return price_usd

if __name__ == '__main__':
    
    print('ticker')
    eth_price_usd = get_ticker("ethereum")
    print('eth_price_usd', eth_price_usd)

