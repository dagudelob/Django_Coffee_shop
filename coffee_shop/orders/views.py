from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Order, OrderItem
from .cart import Cart
from products.models import Product
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from decimal import Decimal


TAX_RATE = Decimal("0.10")  # 10% tax


# ─── Cart Views ───────────────────────────────────────────────────


@login_required
@require_POST
def cart_add(request, product_id):
    """Add a product to the session cart."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, available=True)
    quantity = int(request.POST.get("quantity", 1))
    cart.add(product=product, quantity=quantity)
    messages.success(request, f"'{product.name}' agregado al carrito.")
    return redirect(request.META.get('HTTP_REFERER', 'products:list_product'))


@login_required
def cart_detail(request):
    """Display the current cart with tax calculations."""
    cart = Cart(request)
    cart_items = list(cart)
    subtotal = cart.get_total_price()
    tax = (subtotal * TAX_RATE).quantize(Decimal("0.01"))
    total = subtotal + tax
    return render(
        request,
        "orders/cart.html",
        {
            "cart": cart,
            "cart_items": cart_items,
            "subtotal": subtotal,
            "tax": tax,
            "tax_rate_pct": int(TAX_RATE * 100),
            "total": total,
        },
    )


@login_required
@require_POST
def cart_update(request, product_id):
    """Update the quantity of a product in the cart (set exact quantity)."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get("quantity", 1))
    if quantity <= 0:
        cart.remove(product)
    else:
        cart.add(product=product, quantity=quantity, override_quantity=True)
    return redirect(request.META.get('HTTP_REFERER', 'orders:cart_detail'))


@login_required
@require_POST
def cart_remove(request, product_id):
    """Remove a product entirely from the cart."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f"'{product.name}' eliminado del carrito.")
    return redirect("orders:cart_detail")


# ─── Checkout ─────────────────────────────────────────────────────


@login_required
@require_POST
def checkout(request):
    """Convert the session cart into a persisted Order with OrderItems."""
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "Tu carrito está vacío.")
        return redirect("orders:cart_detail")

    with transaction.atomic():  # type: ignore
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                quantity=item["quantity"],
                price=item["price"],
            )
        cart.clear()

    messages.success(request, f"¡Pedido #{order.id} creado exitosamente!")
    return redirect("orders:my_orders")


# ─── Order History ────────────────────────────────────────────────


@login_required
def my_orders(request):
    """Show the authenticated user's past orders."""
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(
        request, "orders/myorders.html", {"orders": orders, "tax_rate": TAX_RATE}
    )


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(
        request, "orders/myorders.html", {"orders": [order], "tax_rate": TAX_RATE}
    )


# API Views
from rest_framework import generics, permissions
from .serializers import OrderSerializer

class OrderListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # type: ignore
        return Order.objects.filter(user=self.request.user)
