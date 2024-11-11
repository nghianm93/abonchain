import logging
import traceback

from celery import shared_task

from abonchain.arbitrage.exchanges.binance import Binance
from abonchain.arbitrage.exchanges.gateio import GateIO
from abonchain.arbitrage.exchanges.kucoin import KuCoin
from abonchain.arbitrage.exchanges.mexc import MEXC
from abonchain.arbitrage.exchanges.symbol_mapping import SymbolMapping
from abonchain.arbitrage.models import ArbitrageOpportunity


class ArbitrageBot:
    def __init__(self, exchanges, threshold=1.0):
        self.exchanges = exchanges
        self.threshold = threshold

    def fetch_all_prices(self):
        all_data = {}
        for exchange in self.exchanges:
            try:
                all_data[exchange.name] = exchange.fetch_prices()
            except (
                ConnectionError,
                TimeoutError,
                ValueError,
            ):  # Specify common exceptions
                tb = traceback.format_exc()
                logging.exception(tb)
        return all_data

    def check_arbitrage(self, all_data):
        opportunities = []
        exchange_names = list(all_data.keys())

        for i in range(len(exchange_names)):
            for j in range(i + 1, len(exchange_names)):
                exchange1 = exchange_names[i]
                exchange2 = exchange_names[j]

                common_pairs = set(all_data[exchange1].keys()).intersection(
                    set(all_data[exchange2].keys()),
                )

                for pair in common_pairs:
                    data1 = all_data[exchange1].get(pair)
                    data2 = all_data[exchange2].get(pair)

                    if data1 and data2:
                        if data1["bid"] > 0 and 0 < data2["ask"] < data1["bid"]:
                            profit_percent = (
                                (data1["bid"] - data2["ask"]) / data2["ask"] * 100
                            )
                            if profit_percent > self.threshold:
                                opportunity = ArbitrageOpportunity(
                                    exchange_from=exchange2,
                                    exchange_to=exchange1,
                                    trading_pair=pair,
                                    buy_price=data2["ask"],
                                    sell_price=data1["bid"],
                                    profit=profit_percent,
                                )
                                opportunity.save()

                        if data2["bid"] > 0 and 0 < data1["ask"] < data2["bid"]:
                            profit_percent = (
                                (data2["bid"] - data1["ask"]) / data1["ask"] * 100
                            )
                            if profit_percent > self.threshold:
                                opportunity = ArbitrageOpportunity(
                                    exchange_from=exchange1,
                                    exchange_to=exchange2,
                                    trading_pair=pair,
                                    buy_price=data1["ask"],
                                    sell_price=data2["bid"],
                                    profit=profit_percent,
                                )
                                opportunity.save()

        return opportunities

    def run(self):
        all_data = self.fetch_all_prices()
        arbitrage_opps = self.check_arbitrage(all_data)
        return [opp.to_dict() for opp in arbitrage_opps]


@shared_task
def run_arbitrage_bot_task():
    symbol_mapping = SymbolMapping()
    exchanges = [
        Binance("Binance", symbol_mapping),
        KuCoin("KuCoin", symbol_mapping),
        MEXC("MEXC", symbol_mapping),
        GateIO("GateIO", symbol_mapping),
    ]
    bot = ArbitrageBot(exchanges)
    bot.run()
