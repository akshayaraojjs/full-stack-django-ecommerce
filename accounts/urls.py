from django.urls import path
from . import views
from django.http import HttpResponse

# Temporary placeholder views for dashboards
def admin_dashboard(request): return HttpResponse("Admin Dashboard")
def customer_dashboard(request): return HttpResponse("Customer Dashboard")
def seller_dashboard(request): return HttpResponse("Seller Dashboard")

urlpatterns = [
    path('register/customer/', views.register_customer, name='register_customer'),
    path('register/seller/', views.register_seller, name='register_seller'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboards placeholders
    path('dashboard/admin/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/customer/', customer_dashboard, name='customer_dashboard'),
    path('dashboard/seller/', seller_dashboard, name='seller_dashboard'),
]
