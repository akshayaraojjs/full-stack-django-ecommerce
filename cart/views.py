from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from products.models import Product
from .models import Cart, CartItem


def get_or_create_cart(user):
    """Helper: get or create a cart for the logged-in user."""
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@login_required
def cart_detail(request):
    """Display the shopping cart."""
    cart = get_or_create_cart(request.user)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


@login_required
@require_POST
def add_to_cart(request, product_id):
    """Add a product to the cart or increase quantity."""
    product = get_object_or_404(Product, pk=product_id, status='approved')
    cart = get_or_create_cart(request.user)

    quantity = int(request.POST.get('quantity', 1))
    if quantity < 1:
        quantity = 1

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity = min(cart_item.quantity + quantity, product.stock)
    else:
        cart_item.quantity = min(quantity, product.stock)
    cart_item.save()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'"{product.product_name}" added to cart.',
            'cart_count': cart.total_items,
        })

    messages.success(request, f'"{product.product_name}" added to your cart!')
    return redirect('cart_detail')


@login_required
@require_POST
def update_cart(request, item_id):
    """Update quantity of a cart item."""
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))

    if quantity < 1:
        cart_item.delete()
        messages.info(request, 'Item removed from cart.')
    else:
        cart_item.quantity = min(quantity, cart_item.product.stock)
        cart_item.save()
        messages.success(request, 'Cart updated.')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart = get_or_create_cart(request.user)
        return JsonResponse({
            'success': True,
            'subtotal': float(cart_item.subtotal) if quantity >= 1 else 0,
            'cart_total': float(cart.total_price),
            'cart_count': cart.total_items,
        })

    return redirect('cart_detail')


@login_required
def remove_from_cart(request, item_id):
    """Remove a single item from the cart."""
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    product_name = cart_item.product.product_name
    cart_item.delete()
    messages.warning(request, f'"{product_name}" removed from cart.')
    return redirect('cart_detail')


@login_required
def clear_cart(request):
    """Clear all items from the cart."""
    cart = get_or_create_cart(request.user)
    cart.items.all().delete()
    messages.info(request, 'Your cart has been cleared.')
    return redirect('cart_detail')
