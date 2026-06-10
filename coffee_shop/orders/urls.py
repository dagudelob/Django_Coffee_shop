from django.urls import path
from . import views

app_name = "orders"
urlpatterns = [
    # Cart
    path("carrito/", views.cart_detail, name="cart_detail"),
    path("carrito/agregar/<int:product_id>/", views.cart_add, name="cart_add"),
    path("carrito/actualizar/<int:product_id>/", views.cart_update, name="cart_update"),
    path("carrito/eliminar/<int:product_id>/", views.cart_remove, name="cart_remove"),
    path("carrito/checkout/", views.checkout, name="checkout"),
    # Order history
    path("mi-orden/", views.my_orders, name="my_orders"),
    path("<int:pk>/detalle/", views.order_detail, name="detail"),
]
