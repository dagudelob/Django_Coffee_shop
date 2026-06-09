from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, OrderItem
from .forms import OrderCreateForm, OrderItemFormSet
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/myorders.html", {"orders": orders})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, "orders/myorders.html", {"orders": [order]})


@login_required
def order_create(request):
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        formset = OrderItemFormSet(request.POST, prefix="items")

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.user = request.user
                order.save()

                # Create OrderItems
                items = formset.save(commit=False)
                for item in items:
                    item.order = order
                    item.price = item.product.price
                    item.save()

                # Clean up empty items
                for item in formset.deleted_objects:
                    item.delete()

            messages.success(request, "Pedido creado exitosamente.")
            return redirect("orders:detail", pk=order.pk)
        else:
            messages.error(request, "Por favor corrija los errores a continuación.")
    else:
        form = OrderCreateForm()
        formset = OrderItemFormSet(prefix="items")

    return render(
        request,
        "orders/order_form.html",
        {"form": form, "formset": formset, "title": "Nuevo Pedido"},
    )


@login_required
def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)

    if request.method == "POST":
        form = OrderCreateForm(request.POST, instance=order)
        formset = OrderItemFormSet(request.POST, prefix="items", instance=order)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                order = form.save()

                # Update prices for existing items
                for item in formset.save(commit=False):
                    if not item.pk:
                        item.order = order
                    item.price = item.product.price
                    item.save()

                # Clean up empty items
                for item in formset.deleted_objects:
                    item.delete()

            messages.success(request, "Pedido actualizado exitosamente.")
            return redirect("orders:detail", pk=order.pk)
        else:
            messages.error(request, "Por favor corrija los errores a continuación.")
    else:
        form = OrderCreateForm(instance=order)
        formset = OrderItemFormSet(prefix="items", instance=order)

    return render(
        request,
        "orders/order_form.html",
        {"form": form, "formset": formset, "title": "Editar Pedido"},
    )


@login_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)

    if request.method == "POST":
        order.delete()
        messages.success(request, "Pedido eliminado exitosamente.")
        return redirect("orders:list")

    return render(request, "orders/order_confirm_delete.html", {"order": order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/myorders.html", {"orders": orders})
