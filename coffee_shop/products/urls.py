from django.urls import path
from .views import ProductFormView, ProductListView

app_name = "products"
urlpatterns = [
    path("", ProductListView.as_view(), name="list_product"),
    path("agregar/", ProductFormView.as_view(), name="add_product"),
]
