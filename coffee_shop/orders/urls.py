from django.urls import path
from . import views

app_name = "orders"
urlpatterns = [
    path("", views.order_list, name="list"),
    path("mi-orden/", views.my_orders, name="my_orders"),
    path("nuevo/", views.order_create, name="create"),
    path("<int:pk>/detalle/", views.order_detail, name="detail"),
    path("<int:pk>/editar/", views.order_update, name="update"),
    path("<int:pk>/eliminar/", views.order_delete, name="delete"),
]
