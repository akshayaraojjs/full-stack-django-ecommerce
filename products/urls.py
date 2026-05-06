from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('', views.product_list, name='product_list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),

    # Seller
    path('seller/products/', views.seller_product_list, name='seller_product_list'),
    path('seller/products/add/', views.add_product, name='add_product'),
    path('seller/products/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('seller/products/<int:pk>/delete/', views.delete_product, name='delete_product'),

    # Admin
    path('admin/products/', views.admin_product_list, name='admin_product_list'),
    path('admin/products/<int:pk>/approve/', views.approve_product, name='approve_product'),
    path('admin/products/<int:pk>/block/', views.block_product, name='block_product'),
]
