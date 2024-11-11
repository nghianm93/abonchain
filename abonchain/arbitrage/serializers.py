from rest_framework import serializers

from abonchain.arbitrage.models import ArbitrageOpportunity


class ArbitrageOpportunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArbitrageOpportunity
        fields = "__all__"
