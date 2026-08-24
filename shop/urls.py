from django.urls import path

from .views import (
    home,
    menu,
    about,
    contact,
    login_view,
    register_view,
    logout_view,
    product_detail,
    add_to_cart,
    cart_view,
    update_cart,
    remove_from_cart,
    checkout,
    order_success,
    customer_dashboard,
)


urlpatterns = [

    # ============================================================
    # HOME
    # LOGIN REQUIRED
    # ============================================================

    path(
        "",
        home,
        name="home"
    ),


    # ============================================================
    # MENU
    # LOGIN REQUIRED
    # ============================================================

    path(
        "menu/",
        menu,
        name="menu"
    ),


    # ============================================================
    # PRODUCT DETAILS
    # LOGIN REQUIRED
    # ============================================================

    path(
        "product/<int:product_id>/",
        product_detail,
        name="product_detail"
    ),


    # ============================================================
    # ABOUT
    # LOGIN REQUIRED
    # ============================================================

    path(
        "about/",
        about,
        name="about"
    ),


    # ============================================================
    # CONTACT
    # LOGIN REQUIRED
    # ============================================================

    path(
        "contact/",
        contact,
        name="contact"
    ),


    # ============================================================
    # LOGIN
    # PUBLIC
    # ============================================================

    path(
        "login/",
        login_view,
        name="login"
    ),


    # ============================================================
    # REGISTER / CREATE ACCOUNT
    # PUBLIC
    # ============================================================

    path(
        "register/",
        register_view,
        name="register"
    ),


    # ============================================================
    # LOGOUT
    # LOGIN REQUIRED
    # ============================================================

    path(
        "logout/",
        logout_view,
        name="logout"
    ),


    # ============================================================
    # CART
    # LOGIN REQUIRED
    # ============================================================

    path(
        "cart/",
        cart_view,
        name="cart"
    ),


    # ============================================================
    # ADD TO CART
    # LOGIN REQUIRED
    # ============================================================

    path(
        "cart/add/<int:product_id>/",
        add_to_cart,
        name="add_to_cart"
    ),


    # ============================================================
    # UPDATE CART
    # LOGIN REQUIRED
    # ============================================================

    path(
        "cart/update/<int:product_id>/",
        update_cart,
        name="update_cart"
    ),


    # ============================================================
    # REMOVE FROM CART
    # LOGIN REQUIRED
    # ============================================================

    path(
        "cart/remove/<int:product_id>/",
        remove_from_cart,
        name="remove_from_cart"
    ),


    # ============================================================
    # CHECKOUT
    # LOGIN REQUIRED
    # ============================================================

    path(
        "checkout/",
        checkout,
        name="checkout"
    ),


    # ============================================================
    # ORDER SUCCESS
    # LOGIN REQUIRED
    # ============================================================

    path(
        "order-success/<int:order_id>/",
        order_success,
        name="order_success"
    ),


    # ============================================================
    # CUSTOMER DASHBOARD
    # LOGIN REQUIRED
    # ============================================================

    path(
        "dashboard/",
        customer_dashboard,
        name="dashboard"
    ),
]