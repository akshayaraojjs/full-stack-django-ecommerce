from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:product_id>/', views.add_review, name='add_review'),
    path('my-reviews/', views.customer_reviews, name='customer_reviews'),
]
