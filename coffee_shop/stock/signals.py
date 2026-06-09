from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import Product
from orders.models import OrderItem
from .models import Stock, StockTransaction


@receiver(post_save, sender=Product)
def create_product_stock(sender, instance, created, **kwargs):
    if created:
        Stock.objects.get_or_create(product=instance, defaults={"quantity": 0})


@receiver(post_save, sender=StockTransaction)
def update_stock_on_transaction(sender, instance, created, **kwargs):
    if created:
        stock, _ = Stock.objects.get_or_create(
            product=instance.product, defaults={"quantity": 0}
        )
        if instance.transaction_type == "IN":
            stock.quantity += instance.quantity
        elif instance.transaction_type == "OUT":
            stock.quantity = max(0, stock.quantity - instance.quantity)
        stock.save()


@receiver(post_save, sender=OrderItem)
def deduct_stock_on_order(sender, instance, created, **kwargs):
    if created:
        StockTransaction.objects.create(
            product=instance.product,
            transaction_type="OUT",
            quantity=instance.quantity,
            notes=f"Venta en Pedido #{instance.order.id}",
        )
