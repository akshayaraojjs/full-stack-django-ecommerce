from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomerRegistrationForm, SellerRegistrationForm, UserLoginForm, UserUpdateForm, UserProfileForm

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
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return role_based_redirect(request.user)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileForm(instance=request.user.profile)
        
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
    return render(request, 'accounts/dashboards/customer.html')

@login_required
def seller_dashboard(request):
    if request.user.role != 'Seller':
        return redirect('home')
    return render(request, 'accounts/dashboards/seller.html')
