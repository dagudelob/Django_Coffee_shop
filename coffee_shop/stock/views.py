from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from .models import Stock, StockTransaction


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Only allow staff/admin users."""

    def test_func(self):
        return self.request.user.is_staff


class StockDashboardView(StaffRequiredMixin, TemplateView):
    template_name = "stock/stock_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stocks = Stock.objects.select_related("product").all()

        # Calculate statistics
        total_units = stocks.aggregate(total=Sum("quantity"))["total"] or 0
        low_stock_count = stocks.filter(quantity__lt=10).count()

        context["stocks"] = stocks
        context["total_units"] = total_units
        context["low_stock_count"] = low_stock_count
        context["recent_transactions"] = StockTransaction.objects.select_related(
            "product"
        ).order_by("-created_at")[:10]
        return context
