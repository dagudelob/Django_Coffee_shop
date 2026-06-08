from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre")
    description = models.TextField(max_length=300, verbose_name="Descripción")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    image = models.ImageField(upload_to='products/images/', verbose_name="Imagen", null=True, blank=True)
    photo = models.ImageField(upload_to='logos', null=True, blank=True, verbose_name="Foto")
    available = models.BooleanField(default=True, verbose_name="Disponible")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    def __str__(self):
        return self.name