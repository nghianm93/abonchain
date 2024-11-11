class Exchange:
    def __init__(self, name, symbol_mapping):
        self.name = name
        self.symbol_mapping = symbol_mapping

    def fetch_prices(self):
        error_message_price = "Must implement fetch_prices in subclass"
        raise NotImplementedError(error_message_price)

    def get_trade_url(self, pair):
        error_message_url = "Must implement get_trade_url in subclass"
        raise NotImplementedError(error_message_url)
