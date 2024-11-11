from abonchain.arbitrage.arbitrage_bot.arbitrage_bot import ArbitrageBot
from abonchain.arbitrage.exchanges.binance import Binance
from abonchain.arbitrage.exchanges.gateio import GateIO
from abonchain.arbitrage.exchanges.kucoin import KuCoin
from abonchain.arbitrage.exchanges.mexc import MEXC
from abonchain.arbitrage.exchanges.symbol_mapping import SymbolMapping

symbol_mapping = SymbolMapping()
exchanges = [
    Binance("Binance", symbol_mapping),
    KuCoin("KuCoin", symbol_mapping),
    MEXC("MEXC", symbol_mapping),
    GateIO("GateIO", symbol_mapping),
]

bot = ArbitrageBot(exchanges)


# Main function để chạy bot
async def run():
    return await bot.run()
