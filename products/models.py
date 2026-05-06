import uuid
from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    sku_prefix = models.CharField(max_length=10, unique=True, help_text="Short prefix for SKU generation e.g. ELEC, BOOK")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('blocked', 'Blocked'),
    )

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products',
        limit_choices_to={'role': 'Seller'}
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    sku = models.CharField(max_length=20, unique=True, editable=False)
    product_name = models.CharField(max_length=300)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Auto-generate SKU on first save only
        if not self.sku:
            prefix = self.category.sku_prefix if self.category else 'GEN'
            count = Product.objects.filter(category=self.category).count() + 1
            self.sku = f"{prefix}-{count:04d}"
            # Ensure uniqueness if collision
            while Product.objects.filter(sku=self.sku).exists():
                count += 1
                self.sku = f"{prefix}-{count:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_name} ({self.sku})"

    @property
    def primary_image(self):
        img = self.images.first()
        return img.image if img else None


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.product_name}"
