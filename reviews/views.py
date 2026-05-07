from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Review
from orders.models import OrderItem

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check if user has bought this product and order is delivered
    has_bought = OrderItem.objects.filter(
        order__customer=request.user,
        product_name=product.product_name, # Match by name since OrderItem saves snapshot
        order__order_status='delivered'
    ).exists()

    if not has_bought:
        messages.error(request, "You can only review products you have purchased and received.")
        return redirect('product_detail', pk=product.id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        review, created = Review.objects.update_or_create(
            user=request.user,
            product=product,
            defaults={'rating': rating, 'comment': comment}
        )
        
        if created:
            messages.success(request, "Your review has been added!")
        else:
            messages.success(request, "Your review has been updated!")
            
    return redirect('product_detail', pk=product.id)
