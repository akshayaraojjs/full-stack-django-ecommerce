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

### Phase 6: Shopping Cart Module
- **Branch**: `feature/cart-module`
- **Features Completed**:
  - Created `cart` app with `Cart` (OneToOne with User) and `CartItem` models.
  - Add to cart from product detail with quantity picker (respects stock limits).
  - Update quantity (+ / − buttons) per cart item.
  - Remove individual items and clear entire cart.
  - Order summary sidebar with live subtotal per item and cart total.
  - Navbar cart icon with item count badge.
  - AJAX-ready endpoints (`add_to_cart`, `update_cart`) returning JSON responses.
- **Commands Used**:
  - `python manage.py startapp cart`
  - `python manage.py makemigrations cart`
  - `python manage.py migrate`

### Phase 7: Order Management
- **Branch**: `feature/order-management`
- **Features Completed**:
  - Created `orders` app with `Order` and `OrderItem` models.
  - Implemented Checkout flow: captures shipping details, snapshots cart items to order items, deducts stock, and clears cart.
  - **Customer side**: Order History list, Order Detail view, and Order Cancellation (for pending orders).
  - **Seller side**: Dashboard view for "Orders Received", status update capability (Confirmed, Processing, Shipped, Delivered).
  - **Stock Management**: Atomic transactions ensure stock is deducted on purchase and restored on cancellation.
  - **Admin Integration**: Order management with inline item views and status filters in Django Admin.
- **Commands Used**:
  - `python manage.py startapp orders`
  - `python manage.py makemigrations orders`
  - `python manage.py migrate`

### Phase 8: Final Polish & Mock Payment
- **Branch**: `feature/final-polish-deployment`
- **Features Completed**:
  - **Mock Payment Gateway**: Added a processing state to the checkout button using JavaScript and a dedicated "Order Success" landing page.
  - **Premium UI**: Implemented a global design system using the "Outfit" font, sleek glassmorphism navbars, and card hover animations.
  - **Modern Home Page**: Replaced the basic home view with a high-end hero section and feature highlights.
  - **Responsiveness**: Ensured all pages (Cart, Checkout, Dashboards) use Bootstrap's grid for mobile-friendly layouts.
  - **Final Consolidation**: Merged all feature branches into `development` and then into `main`.

### Phase 9: Analytics & UI Polish
- **Branch**: `feature/analytics-polish`
- **Features Completed**:
  - **Dashboard Analytics**: Integrated Chart.js to provide visual insights (Sales per product for Sellers, Spending history for Customers).
  - **Dynamic Metrics**: Implemented real-time counts for Total Orders, Earnings, and Cart items on dashboards.
  - **Role-Based UI**: Restricted "Add to Cart" functionality and Cart Navbar links to Customers only, preventing errors for Sellers/Admins.
  - **Smart Placeholders**: Implemented an external CDN-based placeholder system to ensure all products show an image, even if none is uploaded.
  - **Bug Fixes**: Resolved `RelatedObjectDoesNotExist` errors by protecting Cart access and ensuring `UserProfile` auto-creation.

### Phase 10: Advanced Seller Profiles & Invoicing
- **Branch**: `feature/invoicing-seller-details`
- **Features Completed**:
  - **Enhanced Profiles**: Added GST Number and Business Name fields to Seller profiles.
  - **Company Branding**: Sellers can now upload their Company Logo (via profile image) and Store Address to be used in invoices.
  - **GST Invoicing**: Implemented a dynamic invoice generation system with GST (18%) and Non-GST variants.
  - **Preview & Print**: Created a premium, print-friendly HTML invoice template that customers and sellers can preview and "Print to PDF".
  - **Role-Based Access**: Customers can download invoices for delivered orders, and Sellers can generate them specifically for their products.

### Phase 11: Wishlist, Role-Specific Profiles & UI Refinement
- **Branch**: `feature/final-ui-fixes`
- **Features Completed**:
  - **Wishlist App**: Fully implemented a Wishlist system for Customers to save products for later.
  - **Role-Specific Forms**: Redesigned the "Edit Profile" logic to show business fields (GST/Business Name) only to Sellers, while keeping the Customer view clean.
  - **Cart UX Fix**: Resolved an issue where the quantity number was invisible in the cart. Added `readonly` inputs with +/- controls for better usability.
  - **Clickability Fixes**: Improved CSS `z-index` layering to ensure the Logout button and sidebar items are never overlapped or unclickable.
  - **Template Improvements**: Integrated "Add to Wishlist" heart icons on all product cards and detail pages.

### Phase 12: Advanced Invoicing & Product Review System
- **Branch**: `feature/reviews-and-advanced-invoices`
- **Features Completed**:
  - **Product Reviews**: Implemented a comprehensive rating and review system. Customers can now rate (1-5 stars) and review products they have successfully purchased.
  - **Flipkart-Style Ratings**: Added minimal star ratings and review counts to the product listing cards.
  - **Advanced Invoicing**:
    - **Multi-Seller Splitting**: Invoices now group items by seller and split into separate "pages" with unique branding/logos per seller.
    - **GST Fix**: Corrected GST logic to add the tax amount to the subtotal for the final grand total.
  - **Dynamic Rating Summaries**: Added detailed review lists and average rating badges to the product detail page.

---

## 🚀 Deployment Instructions
1. **Clone the repository**: `git clone <repo-url>`
2. **Setup Virtual Environment**: `python -m venv venv` and `.\venv\Scripts\activate`
3. **Install Dependencies**: `pip install django mysqlclient pillow`
4. **Database Configuration**:
   - Create a MySQL database named `ecommerce_project`.
   - Update `settings.py` with your MySQL credentials.
5. **Run Migrations**: `python manage.py migrate`
6. **Create Admin**: `python manage.py createsuperuser`
7. **Run Server**: `python manage.py run dev`

---

## 🧪 Testing & Seed Data
- To seed the database with 10 categories and 50 approved products for testing:
  - `pip install faker`
  - `python manage.py seed_data`
  - *Note*: If no seller exists, the script will create one with credentials `testseller` / `password123`.

