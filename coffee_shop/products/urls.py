from django.urls import path
from .views import ProductFormView

app_name = 'products'
urlpatterns = [
    path('agregar/', ProductFormView.as_view(), name='add_product'),
]
