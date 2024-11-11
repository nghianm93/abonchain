from django.db import models


class ArbitrageOpportunity(models.Model):
    exchange_from = models.CharField(max_length=10)  # Sàn giao dịch bán
    exchange_to = models.CharField(max_length=10)  # Sàn giao dịch mua
    trading_pair = models.CharField(max_length=20)  # Cặp giao dịch, ví dụ: BTC/USD
    buy_price = models.DecimalField(max_digits=50, decimal_places=20)
    sell_price = models.DecimalField(max_digits=50, decimal_places=20)
    profit = models.DecimalField(max_digits=50, decimal_places=20)
    timestamp = models.DateTimeField(auto_now_add=True)  # Thời gian thu thập dữ liệu

    class Meta:
        app_label = "arbitrage"
        unique_together = ["exchange_from", "exchange_to", "trading_pair"]

    def __str__(self):
        return (
            f"{self.trading_pair} - "
            f"{self.profit}% trên {self.exchange_from} "
            f"và {self.exchange_to}"
        )
