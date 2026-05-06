from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import CustomerRegistrationForm, SellerRegistrationForm, UserLoginForm

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
