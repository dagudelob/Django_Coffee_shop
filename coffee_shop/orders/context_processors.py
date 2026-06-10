from .cart import Cart


def cart_context(request):
    """Make the cart item count available in every template."""
    cart = Cart(request)
    return {"cart_item_count": len(cart)}
