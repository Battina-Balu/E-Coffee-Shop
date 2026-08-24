from django.contrib import admin

from .models import Product, Category, Order


# =========================
# CATEGORY
# =========================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
    )

    search_fields = (
        "name",
    )


# =========================
# PRODUCT
# =========================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "category",
        "price",
        "is_available",
        "is_featured",
    )

    list_filter = (
        "category",
        "is_available",
        "is_featured",
    )

    search_fields = (
        "name",
        "description",
    )


# =========================
# ORDER ACTION
# =========================

@admin.action(description="Confirm selected orders")
def confirm_orders(modeladmin, request, queryset):

    queryset.update(
        status="Confirmed"
    )


# =========================
# ORDER
# =========================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "customer",
        "phone",
        "total_amount",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "customer__username",
        "customer__email",
        "phone",
        "address",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    actions = (
        confirm_orders,
    )