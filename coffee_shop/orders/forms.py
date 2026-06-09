from django import forms
from django.forms import inlineformset_factory
from .models import Order, OrderItem


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = []  # The fields user and created_at are handled automatically


OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    fields=("product", "quantity"),
    extra=1,
    can_delete=True,
)
