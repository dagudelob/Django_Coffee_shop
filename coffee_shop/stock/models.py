from django.db import models
from products.models import Product


class Stock(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="stock", verbose_name="Producto"
    )
    quantity = models.PositiveIntegerField(
        default=0, verbose_name="Cantidad disponible"
    )
    last_updated = models.DateTimeField(
        auto_now=True, verbose_name="Última actualización"
    )

    class Meta:
        verbose_name = "Stock de Producto"
        verbose_name_plural = "Stock de Productos"
        ordering = ["product__name"]

    def __str__(self):
        return f"{self.product.name} ({self.quantity} uds)"


class StockTransaction(models.Model):
    TRANSACTION_TYPES = [
        ("IN", "Entrada (Abastecimiento)"),
        ("OUT", "Salida (Venta/Ajuste)"),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="stock_transactions",
        verbose_name="Producto",
    )
    transaction_type = models.CharField(
        max_length=3, choices=TRANSACTION_TYPES, verbose_name="Tipo de Transacción"
    )
    quantity = models.PositiveIntegerField(verbose_name="Cantidad")
    notes = models.TextField(blank=True, null=True, verbose_name="Notas")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")

    class Meta:
        verbose_name = "Transacción de Stock"
        verbose_name_plural = "Transacciones de Stock"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.product.name} (x{self.quantity})"
