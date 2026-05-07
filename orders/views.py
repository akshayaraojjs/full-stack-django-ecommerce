from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from cart.models import Cart
from .models import Order, OrderItem
from .forms import CheckoutForm


def _get_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


# ── Customer Views ─────────────────────────────────────────────────────────────

@login_required
def checkout(request):
    """Show checkout form pre-filled from profile; on POST place the order."""
    cart = _get_cart(request.user)

    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart_detail')

    # Pre-fill shipping info from profile
    profile = getattr(request.user, 'profile', None)
    initial = {
        'shipping_name':    request.user.username,
        'shipping_phone':   profile.phone    if profile else '',
        'shipping_address': profile.address  if profile else '',
    }

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Create order
                order = Order.objects.create(
                    customer=request.user,
                    total_amount=cart.total_price,
                    order_status='pending',
                    shipping_name=form.cleaned_data['shipping_name'],
                    shipping_phone=form.cleaned_data['shipping_phone'],
                    shipping_address=form.cleaned_data['shipping_address'],
                )

                # Snapshot cart items → order items; deduct stock
                for cart_item in cart.items.select_related('product').all():
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        seller=cart_item.product.seller,
                        product_name=cart_item.product.product_name,
                        sku=cart_item.product.sku,
                        price=cart_item.product.price,
                        quantity=cart_item.quantity,
                    )
                    # Deduct stock
                    cart_item.product.stock -= cart_item.quantity
                    cart_item.product.save(update_fields=['stock'])

                # Clear the cart
                cart.items.all().delete()

            messages.success(request, f'Order #{order.short_uuid} placed successfully!')
            return redirect('order_success', order_uuid=order.order_uuid)
    else:
        form = CheckoutForm(initial=initial)

    return render(request, 'orders/checkout.html', {'form': form, 'cart': cart})


@login_required
def order_success(request, order_uuid):
    """Simple thank you page after order placement."""
    order = get_object_or_404(Order, order_uuid=order_uuid, customer=request.user)
    return render(request, 'orders/success.html', {'order_id': order.short_uuid})


@login_required
def order_history(request):
    """List all orders for the logged-in customer."""
    status_filter = request.GET.get('status')
    orders = Order.objects.filter(customer=request.user).prefetch_related('items').order_by('-created_at')
    
    if status_filter:
        orders = orders.filter(order_status=status_filter)
        
    return render(request, 'orders/order_history.html', {'orders': orders, 'current_status': status_filter})


@login_required
def order_detail(request, order_uuid):
    """Show full detail of a single order."""
    order = get_object_or_404(Order, order_uuid=order_uuid, customer=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def cancel_order(request, order_uuid):
    """Customer can cancel a Pending order."""
    order = get_object_or_404(Order, order_uuid=order_uuid, customer=request.user)
    if order.order_status == 'pending':
        with transaction.atomic():
            # Restore stock
            for item in order.items.select_related('product').all():
                if item.product:
                    item.product.stock += item.quantity
                    item.product.save(update_fields=['stock'])
            order.order_status = 'cancelled'
            order.save()
        messages.warning(request, f'Order #{order.short_uuid} has been cancelled.')
    else:
        messages.error(request, 'Only Pending orders can be cancelled.')
    return redirect('order_history')


# ── Seller Views ──────────────────────────────────────────────────────────────

@login_required
def seller_orders(request):
    """Seller sees orders that contain their products."""
    if request.user.role != 'Seller':
        return redirect('home')

    status_filter = request.GET.get('status')
    # Get unique orders where at least one item belongs to this seller
    order_ids = OrderItem.objects.filter(seller=request.user).values_list('order_id', flat=True).distinct()
    orders = Order.objects.filter(order_uuid__in=order_ids).prefetch_related('items').order_by('-created_at')
    
    if status_filter:
        orders = orders.filter(order_status=status_filter)
        
    return render(request, 'orders/seller/seller_orders.html', {'orders': orders, 'current_status': status_filter})


@login_required
def update_order_status(request, order_uuid):
    """Seller updates the status of an order."""
    if request.user.role != 'Seller':
        return redirect('home')

    order = get_object_or_404(Order, order_uuid=order_uuid)
    if request.method == 'POST':
        new_status = request.POST.get('order_status')
        allowed = ['confirmed', 'processing', 'shipped', 'delivered']
        if new_status in allowed:
            order.order_status = new_status
            order.save()
            messages.success(request, f'Order #{order.short_uuid} status updated to "{new_status}".')
        else:
            messages.error(request, 'Invalid status.')
    return redirect('seller_orders')

@login_required
def generate_invoice(request, order_uuid, invoice_type):
    order = get_object_or_404(Order, order_uuid=order_uuid)
    
    # Base items query
    all_items = order.items.all().select_related('seller', 'seller__profile')
    
    if request.user.role == 'Seller':
        # Seller only sees their own items
        all_items = all_items.filter(seller=request.user)
        if not all_items.exists():
            messages.error(request, "Access denied.")
            return redirect('seller_orders')

    # Group items by seller
    seller_groups = {}
    for item in all_items:
        seller_id = item.seller.id
        if seller_id not in seller_groups:
            seller_groups[seller_id] = {
                'seller': item.seller,
                'items': [],
                'subtotal': 0
            }
        seller_groups[seller_id]['items'].append(item)
        seller_groups[seller_id]['subtotal'] += item.subtotal

    # Calculate tax and total for each group
    for gid in seller_groups:
        group = seller_groups[gid]
        subtotal = float(group['subtotal'])
        if invoice_type == 'gst':
            group['tax_amount'] = round(subtotal * 0.18, 2)
            group['grand_total'] = round(subtotal + group['tax_amount'], 2)
        else:
            group['tax_amount'] = 0
            group['grand_total'] = round(subtotal, 2)

    context = {
        'order': order,
        'seller_groups': seller_groups.values(),
        'invoice_type': invoice_type,
    }
    return render(request, 'orders/invoice_detail.html', context)
