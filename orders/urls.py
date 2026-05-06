from django.urls import path
from . import views

urlpatterns = [
    # Customer
    path('checkout/', views.checkout, name='checkout'),
    path('history/', views.order_history, name='order_history'),
    path('<uuid:order_uuid>/', views.order_detail, name='order_detail'),
    path('<uuid:order_uuid>/cancel/', views.cancel_order, name='cancel_order'),

    # Seller
    path('seller/', views.seller_orders, name='seller_orders'),
    path('seller/<uuid:order_uuid>/update/', views.update_order_status, name='update_order_status'),
]
