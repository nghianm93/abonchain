class SymbolMapping:
    def __init__(self):
        self.symbols = {}

    def add_symbol(self, exchange, original_symbol, formatted_symbol):
        if exchange not in self.symbols:
            self.symbols[exchange] = {}
        self.symbols[exchange][original_symbol] = formatted_symbol

    def get_formatted_symbol(self, exchange, original_symbol):
        return self.symbols.get(exchange, {}).get(original_symbol, original_symbol)
