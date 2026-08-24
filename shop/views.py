from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from .models import Product, Category, Order


# ============================================================
# HOME
# PUBLIC
# ============================================================

def home(request):

    products = Product.objects.filter(
        is_available=True
    ).select_related("category")

    search = request.GET.get("search", "").strip()
    category = request.GET.get("category", "").strip()

    if search:
        products = products.filter(
            name__icontains=search
        )

    if category:
        products = products.filter(
            category__name__iexact=category
        )

    featured_products = products.filter(
        is_featured=True
    )[:6]

    categories = Category.objects.all()

    return render(
        request,
        "shop/home.html",
        {
            "products": products,
            "featured_products": featured_products,
            "categories": categories,
            "search": search,
            "selected_category": category,
        }
    )

# ============================================================
# PRODUCT DETAILS
# LOGIN REQUIRED
# ============================================================

@login_required
def product_detail(request, product_id):

    try:
        product = Product.objects.get(
            id=product_id,
            is_available=True
        )
    except Product.DoesNotExist:
        messages.error(
            request,
            "Product not found or unavailable."
        )
        return redirect("menu")

    return render(
        request,
        "shop/product_detail.html",
        {
            "product": product,
        }
    )
# ============================================================
# MENU
# LOGIN REQUIRED
# ============================================================

@login_required
def menu(request):

    products = Product.objects.filter(
        is_available=True
    ).select_related("category")

    search = request.GET.get(
        "search",
        ""
    ).strip()

    category = request.GET.get(
        "category",
        ""
    ).strip()

    if search:
        products = products.filter(
            name__icontains=search
        )

    if category:
        products = products.filter(
            category__name__iexact=category
        )

    categories = Category.objects.all()

    return render(
        request,
        "shop/menu.html",
        {
            "products": products,
            "categories": categories,
            "search": search,
            "selected_category": category,
        }
    )

# ============================================================
# ABOUT
# PUBLIC
# ============================================================

def about(request):

    return render(
        request,
        "shop/about.html"
    )


# ============================================================
# CONTACT
# PUBLIC
# ============================================================

def contact(request):

    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        message_text = request.POST.get(
            "message",
            ""
        ).strip()

        if not name or not email or not message_text:

            messages.error(
                request,
                "Please fill in all fields."
            )

            return render(
                request,
                "shop/contact.html"
            )

        messages.success(
            request,
            "Thank you! Your message has been received."
        )

        return redirect("contact")

    return render(
        request,
        "shop/contact.html"
    )


# ============================================================
# LOGIN
# PUBLIC
# ============================================================

def login_view(request):

    # Already logged-in user
    if request.user.is_authenticated:
        return redirect("home")

    # Requested page before login
    next_url = request.GET.get("next", "")

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        # Keep next URL from hidden form field
        next_url = request.POST.get(
            "next",
            next_url
        )

        if not username or not password:

            messages.error(
                request,
                "Please enter username and password."
            )

            return render(
                request,
                "shop/login.html",
                {
                    "next": next_url
                }
            )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            # Safely return to requested page
            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure()
            ):
                return redirect(next_url)

            return redirect("home")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "shop/login.html",
        {
            "next": next_url
        }
    )


# ============================================================
# REGISTER / CREATE ACCOUNT
# PUBLIC
# ============================================================

def register_view(request):

    # Already logged-in user
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        confirm_password = request.POST.get(
            "confirm_password",
            ""
        )

        # ----------------------------------------------------
        # Empty fields
        # ----------------------------------------------------

        if not username or not email or not password or not confirm_password:

            messages.error(
                request,
                "Please fill in all fields."
            )

            return render(
                request,
                "shop/register.html"
            )

        # ----------------------------------------------------
        # Password confirmation
        # ----------------------------------------------------

        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return render(
                request,
                "shop/register.html"
            )

        # ----------------------------------------------------
        # Username already exists
        # ----------------------------------------------------

        if User.objects.filter(
            username__iexact=username
        ).exists():

            messages.error(
                request,
                "Username already exists. Please choose another username."
            )

            return render(
                request,
                "shop/register.html"
            )

        # ----------------------------------------------------
        # Email already exists
        # ----------------------------------------------------

        if User.objects.filter(
            email__iexact=email
        ).exists():

            messages.error(
                request,
                "This email is already registered."
            )

            return render(
                request,
                "shop/register.html"
            )

        # ----------------------------------------------------
        # Create user
        # ----------------------------------------------------

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # ----------------------------------------------------
        # Login automatically after registration
        # ----------------------------------------------------

        login(
            request,
            user
        )

        messages.success(
            request,
            "Account created successfully. Welcome to E-Coffee!"
        )

        return redirect("home")

    return render(
        request,
        "shop/register.html"
    )


# ============================================================
# LOGOUT
# PUBLIC
# ============================================================

def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("login")


# ============================================================
# ADD TO CART
# LOGIN REQUIRED
# ============================================================

@login_required
def add_to_cart(request, product_id):

    cart = request.session.get(
        "cart",
        {}
    )

    product_id = str(product_id)

    # Make sure product exists and is available
    try:

        Product.objects.get(
            id=product_id,
            is_available=True
        )

    except Product.DoesNotExist:

        messages.error(
            request,
            "Product is not available."
        )

        return redirect("home")

    if product_id in cart:

        cart[product_id] += 1

    else:

        cart[product_id] = 1

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


# ============================================================
# CART
# LOGIN REQUIRED
# ============================================================

@login_required
def cart_view(request):

    cart = request.session.get(
        "cart",
        {}
    )

    cart_items = []
    total = 0

    for product_id, quantity in cart.items():

        try:

            product = Product.objects.get(
                id=product_id,
                is_available=True
            )

        except Product.DoesNotExist:

            continue

        subtotal = product.price * quantity

        total += subtotal

        cart_items.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )

    return render(
        request,
        "shop/cart.html",
        {
            "cart_items": cart_items,
            "total": total,
        }
    )


# ============================================================
# UPDATE CART
# LOGIN REQUIRED
# ============================================================

@login_required
def update_cart(request, product_id):

    if request.method == "POST":

        cart = request.session.get(
            "cart",
            {}
        )

        product_id = str(product_id)

        action = request.POST.get(
            "action"
        )

        if product_id in cart:

            if action == "increase":

                cart[product_id] += 1

            elif action == "decrease":

                cart[product_id] -= 1

                if cart[product_id] <= 0:

                    del cart[product_id]

        request.session["cart"] = cart
        request.session.modified = True

    return redirect("cart")


# ============================================================
# REMOVE FROM CART
# LOGIN REQUIRED
# ============================================================

@login_required
def remove_from_cart(request, product_id):

    if request.method == "POST":

        cart = request.session.get(
            "cart",
            {}
        )

        product_id = str(product_id)

        if product_id in cart:

            del cart[product_id]

        request.session["cart"] = cart
        request.session.modified = True

    return redirect("cart")


# ============================================================
# CHECKOUT
# LOGIN REQUIRED
# ============================================================

@login_required
def checkout(request):

    cart = request.session.get(
        "cart",
        {}
    )

    if not cart:

        return redirect("cart")

    cart_items = []
    total = 0

    for product_id, quantity in cart.items():

        try:

            product = Product.objects.get(
                pk=product_id,
                is_available=True
            )

        except Product.DoesNotExist:

            continue

        subtotal = product.price * quantity

        total += subtotal

        cart_items.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )

    if not cart_items:

        request.session["cart"] = {}
        request.session.modified = True

        return redirect("cart")

    # --------------------------------------------------------
    # PLACE ORDER
    # --------------------------------------------------------

    if request.method == "POST":

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        address = request.POST.get(
            "address",
            ""
        ).strip()

        if not phone or not address:

            messages.error(
                request,
                "Please enter your phone number and address."
            )

            return render(
                request,
                "shop/checkout.html",
                {
                    "cart_items": cart_items,
                    "total": total,
                }
            )

        order = Order.objects.create(
            customer=request.user,
            phone=phone,
            address=address,
            total_amount=total,
        )

        # Clear cart
        request.session["cart"] = {}
        request.session.modified = True

        return redirect(
            "order_success",
            order_id=order.id
        )

    return render(
        request,
        "shop/checkout.html",
        {
            "cart_items": cart_items,
            "total": total,
        }
    )


# ============================================================
# ORDER SUCCESS
# LOGIN REQUIRED
# ============================================================

@login_required
def order_success(request, order_id):

    try:

        order = Order.objects.get(
            id=order_id,
            customer=request.user
        )

    except Order.DoesNotExist:

        return redirect("home")

    return render(
        request,
        "shop/order_success.html",
        {
            "order": order
        }
    )


# ============================================================
# CUSTOMER DASHBOARD
# LOGIN REQUIRED
# ============================================================

@login_required
def customer_dashboard(request):

    orders = Order.objects.filter(
        customer=request.user
    ).order_by(
        "-created_at"
    )

    total_orders = orders.count()

    total_spent = sum(
        order.total_amount
        for order in orders
    )

    return render(
        request,
        "shop/dashboard.html",
        {
            "orders": orders,
            "total_orders": total_orders,
            "total_spent": total_spent,
        }
    )