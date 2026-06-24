from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from decimal import Decimal


TAX_RATE = Decimal("0.10")


class Order(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Pedido #{self.pk} - {self.user.username}"  # type: ignore

    @property
    def total_value(self):
        return sum(item.total_price for item in self.items.all())  # type: ignore

    @property
    def tax_amount(self):
        return (self.total_value * TAX_RATE).quantize(Decimal("0.01"))

    @property
    def total_with_tax(self):
        return self.total_value + self.tax_amount


class OrderItem(models.Model):
    objects = models.Manager()
    order = models.ForeignKey(
        Order, related_name="items", on_delete=models.CASCADE, verbose_name="Pedido"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Producto"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Cantidad")  # type: ignore
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")

    class Meta:
        verbose_name = "Ítem de Pedido"
        verbose_name_plural = "Ítems de Pedido"

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

    @property
    def total_price(self):
        return self.quantity * self.price  # type: ignore
