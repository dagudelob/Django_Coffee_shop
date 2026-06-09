from django.urls import path
from .views import StockDashboardView

app_name = "stock"

urlpatterns = [
    path("", StockDashboardView.as_view(), name="dashboard"),
]
