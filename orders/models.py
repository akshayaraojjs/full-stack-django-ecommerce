import uuid
from django.db import models
from django.conf import settings
from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending',    'Pending'),
        ('confirmed',  'Confirmed'),
        ('processing', 'Processing'),
        ('shipped',    'Shipped'),
        ('delivered',  'Delivered'),
        ('cancelled',  'Cancelled'),
    )

    order_uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders'
    )
    total_amount  = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    order_status  = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Shipping address snapshot (captured at order time)
    shipping_name    = models.CharField(max_length=200)
    shipping_phone   = models.CharField(max_length=20)
    shipping_address = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {str(self.order_uuid)[:8]} — {self.customer}"

    @property
    def short_uuid(self):
        return str(self.order_uuid)[:8].upper()


class OrderItem(models.Model):
    """Immutable snapshot of a product at order time."""
    order          = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product        = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='order_items')
    seller         = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='sold_items'
    )
    product_name   = models.CharField(max_length=300)   # snapshot
    sku            = models.CharField(max_length=20)     # snapshot
    price          = models.DecimalField(max_digits=10, decimal_places=2)  # snapshot
    quantity       = models.PositiveIntegerField()

    @property
    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} × {self.product_name} in Order {self.order.short_uuid}"
