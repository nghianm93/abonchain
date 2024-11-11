import requests

from abonchain.arbitrage.exchanges.exchange import Exchange


class GateIO(Exchange):
    def fetch_prices(self):
        url = "https://api.gateio.ws/api/v4/spot/tickers"
        response = requests.get(url, timeout=10)
        prices = {}

        for item in response.json():
            bid = item["highest_bid"]
            ask = item["lowest_ask"]
            if (
                bid is not None
                and ask is not None
                and bid
                and ask
                and bid.strip()
                and ask.strip()
            ):
                symbol = item["currency_pair"].replace("_", "")
                prices[symbol] = {
                    "bid": float(item["highest_bid"]),
                    "ask": float(item["lowest_ask"]),
                }
                formatted_symbol = (
                    symbol[: len(symbol) - 4] + "_" + symbol[-4:]
                )  # BTC_USDT
                self.symbol_mapping.add_symbol(self.name, symbol, formatted_symbol)

        return prices

    def get_trade_url(self, pair):
        formatted_pair = self.symbol_mapping.get_formatted_symbol(self.name, pair)
        return f"https://www.gate.io/trade/{formatted_pair}"
