from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomerRegistrationForm, SellerRegistrationForm, UserLoginForm, UserUpdateForm

def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Customer account created successfully. Please login.')
            return redirect('login')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form, 'title': 'Customer Registration'})

def register_seller(request):
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Seller account created successfully. Please login.')
            return redirect('login')
    else:
        form = SellerRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form, 'title': 'Seller Registration'})

def login_view(request):
    if request.user.is_authenticated:
        return role_based_redirect(request.user)
        
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return role_based_redirect(user)
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

def role_based_redirect(user):
    if user.role == 'Admin' or user.is_superuser:
        return redirect('admin_dashboard')
    elif user.role == 'Seller':
        return redirect('seller_dashboard')
    else:
        return redirect('customer_dashboard')

@login_required
def edit_profile(request):
    from .models import UserProfile
    from .forms import UserUpdateForm, CustomerProfileForm, SellerProfileForm
    
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Select form based on user role
    FormClass = SellerProfileForm if request.user.role == 'Seller' else CustomerProfileForm

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = FormClass(request.POST, request.FILES, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return role_based_redirect(request.user)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = FormClass(instance=profile)
        
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': 'Edit Profile'
    }
    return render(request, 'accounts/profile_edit.html', context)

@login_required
def admin_dashboard(request):
    if request.user.role != 'Admin' and not request.user.is_superuser:
        return redirect('home')
    return render(request, 'accounts/dashboards/admin.html')

@login_required
def customer_dashboard(request):
    if request.user.role != 'Customer':
        return redirect('home')
    
    from orders.models import Order
    from cart.models import Cart
    
    orders = Order.objects.filter(customer=request.user)
    total_orders = orders.count()
    total_spent = sum(o.total_amount for o in orders if o.order_status != 'cancelled')
    
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.count()
    
    # Simple stats for Chart.js (last 5 orders)
    recent_orders = orders.order_by('-created_at')[:5]
    chart_labels = [o.created_at.strftime('%d %b') for o in reversed(recent_orders)]
    chart_data = [float(o.total_amount) for o in reversed(recent_orders)]
    
    context = {
        'total_orders': total_orders,
        'total_spent': total_spent,
        'cart_items': cart_items,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }
    return render(request, 'accounts/dashboards/customer.html', context)

@login_required
def seller_dashboard(request):
    if request.user.role != 'Seller':
        return redirect('home')
    
    from products.models import Product
    from orders.models import OrderItem, Order
    
    my_products = Product.objects.filter(seller=request.user)
    total_products = my_products.count()
    
    # Orders containing this seller's products
    my_order_items = OrderItem.objects.filter(seller=request.user)
    # Get distinct orders from these items
    order_ids = my_order_items.values_list('order_id', flat=True).distinct()
    my_orders = Order.objects.filter(order_uuid__in=order_ids)
    
    pending_orders = my_orders.filter(order_status='pending').count()
    total_earnings = sum(item.subtotal for item in my_order_items if item.order.order_status != 'cancelled')
    
    # Stats for Chart.js (Earnings per product - Top 5)
    from django.db.models import Sum
    top_products = my_order_items.values('product_name').annotate(total_sales=Sum('quantity')).order_by('-total_sales')[:5]
    chart_labels = [p['product_name'] for p in top_products]
    chart_data = [p['total_sales'] for p in top_products]
    
    context = {
        'total_products': total_products,
        'pending_orders': pending_orders,
        'total_earnings': total_earnings,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }
    return render(request, 'accounts/dashboards/seller.html', context)
