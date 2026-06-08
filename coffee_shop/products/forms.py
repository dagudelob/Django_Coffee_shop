from django import forms
from .models import Product


class ProductForm(forms.Form):
    name = forms.CharField(max_length=200, required=True, label="Nombre")
    description = forms.CharField(
        widget=forms.Textarea, max_length=300, required=True, label="Descripción"
    )
    price = forms.DecimalField(
        max_digits=10, decimal_places=2, required=True, label="Precio"
    )
    image = forms.ImageField(required=False, label="Imagen")
    photo = forms.ImageField(required=False, label="Foto")
    available = forms.BooleanField(initial=True, required=False, label="Disponible")

    def save(self):
        # Aquí está la lógica de negocio explícita que te gusta:
        # Tomamos los datos limpios y creamos el registro en la base de datos.
        product = Product.objects.create(
            name=self.cleaned_data["name"],
            description=self.cleaned_data["description"],
            price=self.cleaned_data["price"],
            image=self.cleaned_data["image"],
            photo=self.cleaned_data["photo"],
            available=self.cleaned_data["available"],
        )
        # Es MUY importante retornar el objeto creado para que la vista sepa que todo salió bien
        return product
