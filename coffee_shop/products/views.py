from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import ProductForm
from .models import Product


class ProductListView(generic.ListView):
    model = Product
    template_name = "products/list_product.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from orders.cart import Cart
        cart = Cart(self.request)
        for product in context["products"]:
            product.cart_quantity = cart.cart.get(str(product.id), {}).get("quantity", 0)
        return context


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Only allow staff/admin users."""
    def test_func(self):
        return self.request.user.is_staff  # type: ignore


class ProductFormView(StaffRequiredMixin, generic.FormView):
    template_name = "products/add_product.html"
    form_class = ProductForm
    success_url = reverse_lazy("products:list_product")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# API Views
from rest_framework import generics, permissions
from .serializers import ProductSerializer

class IsStaffOrReadOnly(permissions.BasePermission):
    """Permission class to allow only staff to modify products, but anyone to read."""
    def has_permission(self, request, view):  # type: ignore
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsStaffOrReadOnly]
