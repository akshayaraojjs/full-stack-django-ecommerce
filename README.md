# full-stack-django-ecommerce
Building Full Stack Django Ecommerce Application 

## Project Tracking

### Phase 1: Project Initialization
- **Branch**: `feature/project-setup`
- **Features Completed**:
  - Initialized Git repository and branching strategy.
  - Setup virtual environment and installed dependencies.
  - Configured Django project (`ecommerce_project`) and MySQL database.
  - Implemented base Bootstrap 5 template (`base.html`), navbar, and footer.
- **Commands Used**:
  - `django-admin startproject ecommerce_project .`
  - `python manage.py migrate`

### Phase 2: Authentication & Role-Based Login
- **Branch**: `feature/authentication`
- **Features Completed**:
  - Created `accounts` app.
  - Custom User model (`AbstractBaseUser`) with UUID primary keys and `role` (Admin, Customer, Seller).
  - Configured `AUTH_USER_MODEL = 'accounts.User'`.
  - Registration forms (Customer, Seller) and Login forms with Bootstrap styling.
  - Login, Logout, and role-based redirects.
  - Monkey-patched Django to support MariaDB 10.4.x (XAMPP).
- **Commands Used**:
  - `python manage.py startapp accounts`
  - `python manage.py makemigrations accounts`
  - `python manage.py migrate`

### Phase 3: User Profile Management
- **Branch**: `feature/user-management`
- **Features Completed**:
  - Created `UserProfile` model (OneToOne relationship with `User`).
  - Added `post_save` signals to auto-create profiles on User creation.
  - Created `UserUpdateForm` and `UserProfileForm`.
  - Built `edit_profile` view for updating phone, address, and profile image.
  - Designed interactive role-based dashboards (`admin.html`, `customer.html`, `seller.html`).
  - Configured `MEDIA_URL` and `MEDIA_ROOT` for handling uploaded images.
- **Commands Used**:
  - `python manage.py makemigrations accounts`
  - `python manage.py migrate`

### Phase 4: Product Management
- **Branch**: `feature/product-management`
- **Features Completed**:
  - Created `products` app with `Category`, `Product`, and `ProductImage` models.
  - Auto-generated SKU using category prefix and count (e.g. `ELEC-0001`, `BOOK-0002`).
  - Seller-side: Add, Edit, Delete product & upload multiple images.
  - Admin-side: View all products, Approve or Block products.
  - Public: Product listing page (approved only) and product detail page.
  - Registered all models in Django Admin with inline image management.
- **Commands Used**:
  - `python manage.py startapp products`
  - `python manage.py makemigrations products`
  - `python manage.py migrate`

### Bug Fixes (Post Phase 4)
- **Branch**: `feature/search-filter`
- **Fixes**:
  - Fixed `RelatedObjectDoesNotExist` error on Edit Profile page by using `get_or_create` for `UserProfile`.
  - Wired up Seller dashboard sidebar: **My Products** → `/products/seller/products/`, **Add Product** → `/products/seller/products/add/`.
  - Wired up Admin dashboard sidebar: **Approve Products** → `/products/admin/products/`.

### Phase 5: Product Listing & Search
- **Branch**: `feature/search-filter`
- **Features Completed**:
  - Dynamic search by product name with 600ms debounce (live search on keyup).
  - Filter by category (sidebar links).
  - Filter by price range (min/max inputs).
  - Sort by: Newest, Oldest, Price Low→High, Price High→Low.
  - Pagination (9 products per page) with filter state preserved across pages.
  - Active filter state shown in sidebar and toolbar.
