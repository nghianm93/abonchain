import requests

from abonchain.arbitrage.exchanges.exchange import Exchange


class Binance(Exchange):
    def fetch_prices(self):
        url = "https://api.binance.com/api/v3/ticker/bookTicker"
        response = requests.get(url, timeout=10)
        prices = {
            item["symbol"]: {
                "bid": float(item["bidPrice"]),
                "ask": float(item["askPrice"]),
            }
            for item in response.json()
        }
        for symbol in prices:
            self.symbol_mapping.add_symbol(self.name, symbol, symbol)
        return prices

    def get_trade_url(self, pair):
        formatted_pair = self.symbol_mapping.get_formatted_symbol(self.name, pair)
        return f"https://www.binance.com/en/trade/{formatted_pair}"
