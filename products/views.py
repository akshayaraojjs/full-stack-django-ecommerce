from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, ProductImage, Category
from .forms import ProductForm, ProductImageForm


def product_list(request):
    """Public product listing with search, filter, sort, and pagination."""
    from django.core.paginator import Paginator

    products = Product.objects.filter(status='approved').select_related('category', 'seller')
    categories = Category.objects.all()

    # Search by name
    query = request.GET.get('q', '').strip()
    if query:
        products = products.filter(product_name__icontains=query)

    # Filter by category slug
    cat_slug = request.GET.get('category', '')
    if cat_slug:
        products = products.filter(category__slug=cat_slug)

    # Filter by price range
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    # Sort
    sort = request.GET.get('sort', '')
    sort_options = {
        'price_asc': 'price',
        'price_desc': '-price',
        'newest': '-created_at',
        'oldest': 'created_at',
    }
    products = products.order_by(sort_options.get(sort, '-created_at'))

    # Pagination — 9 products per page
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Wishlist context
    wishlisted_product_ids = []
    if request.user.is_authenticated and request.user.role == 'Customer':
        from wishlist.models import Wishlist
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        wishlisted_product_ids = wishlist.products.values_list('id', flat=True)

    return render(request, 'products/product_list.html', {
        'page_obj': page_obj,
        'products': page_obj,
        'categories': categories,
        'query': query,
        'cat_slug': cat_slug,
        'min_price': min_price,
        'max_price': max_price,
        'sort': sort,
        'wishlisted_product_ids': wishlisted_product_ids,
    })


def product_detail(request, pk):
    """Public product detail page."""
    product = get_object_or_404(Product, pk=pk, status='approved')
    
    is_wishlisted = False
    if request.user.is_authenticated and request.user.role == 'Customer':
        from wishlist.models import Wishlist
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        is_wishlisted = wishlist.products.filter(id=product.id).exists()

    return render(request, 'products/product_detail.html', {
        'product': product,
        'is_wishlisted': is_wishlisted
    })


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
