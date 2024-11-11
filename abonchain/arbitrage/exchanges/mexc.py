import requests

from abonchain.arbitrage.exchanges.exchange import Exchange


class MEXC(Exchange):
    def fetch_prices(self):
        url = "https://www.mexc.com/open/api/v2/market/ticker"
        response = requests.get(url, timeout=10)
        prices = {
            item["symbol"].replace("_", ""): {
                "bid": float(item["bid"]),
                "ask": float(item["ask"]),
            }
            for item in response.json()["data"]
        }
        for symbol in prices:
            formatted_symbol = symbol[: len(symbol) - 4] + "_" + symbol[-4:]
            self.symbol_mapping.add_symbol(self.name, symbol, formatted_symbol)
        return prices

    def get_trade_url(self, pair):
        formatted_pair = self.symbol_mapping.get_formatted_symbol(self.name, pair)
        return f"https://www.mexc.com/exchange/{formatted_pair}"
