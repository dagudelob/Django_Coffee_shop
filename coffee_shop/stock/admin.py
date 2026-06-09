from django.contrib import admin
from .models import Stock, StockTransaction


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity", "last_updated")
    search_fields = ("product__name",)
    list_filter = ("last_updated",)


@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ("product", "transaction_type", "quantity", "created_at")
    list_filter = ("transaction_type", "created_at")
    search_fields = ("product__name", "notes")
