from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import ProductForm
from .models import Product


class ProductListView(generic.ListView):
    model = Product
    template_name = "products/list_product.html"
    context_object_name = "products"


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Only allow staff/admin users."""
    def test_func(self):
        return self.request.user.is_staff


class ProductFormView(StaffRequiredMixin, generic.FormView):
    template_name = "products/add_product.html"
    form_class = ProductForm
    success_url = reverse_lazy("products:list_product")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
