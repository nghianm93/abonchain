from django.contrib import admin

from .models import ArbitrageOpportunity


# Define the admin class
@admin.register(ArbitrageOpportunity)
class ArbitrageOpportunityAdmin(admin.ModelAdmin):
    pass
