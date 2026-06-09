from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "created_at", "get_total_value"]
    list_filter = ["created_at", "user"]
    search_fields = ["user__username", "user__email"]
    raw_id_fields = ["user"]
    inlines = [OrderItemInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["initial"] = request.user.id
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_total_value(self, obj):
        return f"${obj.total_value}"

    get_total_value.short_description = "Valor Total"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "product", "quantity", "price", "get_total_price"]

    def get_total_price(self, obj):
        return f"${obj.total_price}"

    get_total_price.short_description = "Precio Total"
