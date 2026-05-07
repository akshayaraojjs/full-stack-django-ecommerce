import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
from accounts.models import User
from products.models import Category, Product, ProductImage

class Command(BaseCommand):
    help = 'Seed the database with 10 categories and 50 products'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        self.stdout.write("Seeding data...")

        # 1. Ensure at least one seller exists
        seller = User.objects.filter(role='Seller').first()
        if not seller:
            seller = User.objects.create_user(
                username='testseller',
                email='seller@example.com',
                password='password123',
                role='Seller'
            )
            self.stdout.write(f"Created default seller: {seller.username}")

        # 2. Create 10 Categories
        category_data = [
            ('Electronics', 'ELEC'),
            ('Fashion', 'FASH'),
            ('Home & Kitchen', 'HOME'),
            ('Books', 'BOOK'),
            ('Beauty', 'BEAU'),
            ('Sports', 'SPOR'),
            ('Toys', 'TOYS'),
            ('Automotive', 'AUTO'),
            ('Groceries', 'GROC'),
            ('Health', 'HEAL'),
        ]

        categories = []
        for name, prefix in category_data:
            cat, created = Category.objects.get_or_create(
                name=name,
                defaults={
                    'slug': slugify(name),
                    'sku_prefix': prefix
                }
            )
            categories.append(cat)
            if created:
                self.stdout.write(f"Created category: {name}")

        # 3. Create 50 Products
        for i in range(50):
            category = random.choice(categories)
            # Use a combination of words to ensure unique-ish names
            product_name = f"{fake.word().capitalize()} {fake.word().capitalize()} {random.randint(100, 999)}"
            
            product = Product.objects.create(
                seller=seller,
                category=category,
                product_name=product_name,
                description=fake.paragraph(nb_sentences=3),
                price=random.randint(100, 10000),
                stock=random.randint(5, 100),
                status='approved'
            )
            
            # Note: We won't seed actual images here because it requires files, 
            # but the UI handles missing images gracefully.
            
            if (i + 1) % 10 == 0:
                self.stdout.write(f"Created {i + 1} products...")

        self.stdout.write(self.style.SUCCESS("Successfully seeded 10 categories and 50 products!"))
