from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, ProductImage, Category
from .forms import ProductForm, ProductImageForm


def product_list(request):
    """Public product listing page — shows only approved products."""
    products = Product.objects.filter(status='approved').select_related('category', 'seller')
    categories = Category.objects.all()
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
    })


def product_detail(request, pk):
    """Public product detail page."""
    product = get_object_or_404(Product, pk=pk, status='approved')
    return render(request, 'products/product_detail.html', {'product': product})


# ─── Seller Views ─────────────────────────────────────────────────────────────

def seller_required(view_func):
    """Decorator to restrict access to Sellers only."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'Seller':
            messages.error(request, 'Access denied. Seller account required.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@seller_required
def seller_product_list(request):
    """Seller's own products listing."""
    products = Product.objects.filter(seller=request.user)
    return render(request, 'products/seller/product_list.html', {'products': products})


@login_required
@seller_required
def add_product(request):
    """Seller adds a new product."""
    if request.method == 'POST':
        form = ProductForm(request.POST)
        img_form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            if img_form.is_valid() and request.FILES.get('image'):
                image = img_form.save(commit=False)
                image.product = product
                image.save()
            messages.success(request, f'Product "{product.product_name}" added successfully! Awaiting admin approval.')
            return redirect('seller_product_list')
    else:
        form = ProductForm()
        img_form = ProductImageForm()
    return render(request, 'products/seller/product_form.html', {
        'form': form, 'img_form': img_form, 'title': 'Add Product'
    })


@login_required
@seller_required
def edit_product(request, pk):
    """Seller edits their own product."""
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('seller_product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/seller/product_form.html', {
        'form': form, 'img_form': ProductImageForm(), 'title': 'Edit Product', 'product': product
    })


@login_required
@seller_required
def delete_product(request, pk):
    """Seller deletes their own product."""
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('seller_product_list')
    return render(request, 'products/seller/product_confirm_delete.html', {'product': product})


# ─── Admin Views ───────────────────────────────────────────────────────────────

def admin_required(view_func):
    """Decorator to restrict access to Admins only."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or (request.user.role != 'Admin' and not request.user.is_superuser):
            messages.error(request, 'Access denied. Admin account required.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@admin_required
def admin_product_list(request):
    """Admin sees all products and can approve/block them."""
    products = Product.objects.all().select_related('category', 'seller')
    return render(request, 'products/admin/product_list.html', {'products': products})


@login_required
@admin_required
def approve_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.status = 'approved'
    product.save()
    messages.success(request, f'Product "{product.product_name}" has been approved.')
    return redirect('admin_product_list')


@login_required
@admin_required
def block_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.status = 'blocked'
    product.save()
    messages.warning(request, f'Product "{product.product_name}" has been blocked.')
    return redirect('admin_product_list')
