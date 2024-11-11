from django.urls import path

from . import views
from .views import ArbitrageOpportunityListView

urlpatterns = [
    path("run-bot/", views.run_arbitrage_bot, name="run_arbitrage_bot"),
    path(
        "opportunities/",
        ArbitrageOpportunityListView.as_view(),
        name="opportunity_list",
    ),
]
