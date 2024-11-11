import requests

from abonchain.arbitrage.exchanges.exchange import Exchange


class KuCoin(Exchange):
    def fetch_prices(self):
        url = "https://api.kucoin.com/api/v1/market/allTickers"
        response = requests.get(url, timeout=10)
        prices = {}

        for item in response.json()["data"]["ticker"]:
            if item["buy"] is not None and item["sell"] is not None:
                symbol = item["symbol"].replace("-", "")
                prices[symbol] = {
                    "bid": float(item["buy"]),
                    "ask": float(item["sell"]),
                }
                formatted_symbol = (
                    symbol[: len(symbol) - 4] + "-" + symbol[-4:]
                )  # BTC-USDT
                self.symbol_mapping.add_symbol(self.name, symbol, formatted_symbol)

        return prices

    def get_trade_url(self, pair):
        formatted_pair = self.symbol_mapping.get_formatted_symbol(self.name, pair)
        return f"https://www.kucoin.com/trade/{formatted_pair}"
