from django.contrib import admin
from .models import UserInfo, Category, Product, Cart, CartItem, Order, OrderItem, DeliveryInfo


# Register your models here.

def get_readonly_fields(self, request, obj=None):
    if not request.user.is_superuser and not request.user.is_staff:
        return [f.name for f in self.model._meta.fields]
    return super().get_readonly_fields(request, obj)


def get_queryset(self, request):
    if request.user.is_superuser or request.user.is_staff:
        return super().get_queryset(request)
    return self.model.objects.none()


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    search_fields = ['user__username', 'user__email', 'role']

    def has_add_permission(self, request):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False

    def has_change_permission(self, request, obj: UserInfo | None = None):
        if obj is not None and obj.user == request.user:
            return True
        if obj is None and (request.user.is_superuser or request.user.is_staff):
            return True
        return False

    def has_delete_permission(self, request, obj: UserInfo | None = None):
        if self.has_change_permission(request, obj):
            return True
        return False

    def has_view_permission(self, request, obj: UserInfo | None = None):
        if request.user.is_authenticated:
            return True
        return False


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'image', 'createdDate']
    search_fields = ['name', 'description', 'price', 'category__name', 'user__username']
    list_filter = ['id', 'price', 'category', 'user']

    def has_add_permission(self, request):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False

    def has_change_permission(self, request, _: Product | None = None):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False

    def has_delete_permission(self, request, _: Product | None = None):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False

    def has_view_permission(self, request, _: Product | None = None):
        if request.user.is_authenticated:
            return True
        return False


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

    def has_add_permission(self, request):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False

    def has_change_permission(self, request, _: Category | None = None):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False

    def has_delete_permission(self, request, _: Category | None = None):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False

    def has_view_permission(self, request, _: Category | None = None):
        if request.user.is_authenticated:
            return True
        return False


class CartAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user__username']

    def has_add_permission(self, request):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False

    def has_change_permission(self, request, _: Cart | None = None):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False

    def has_delete_permission(self, request, _: Cart | None = None):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False

    def has_view_permission(self, request, _: Cart | None = None):
        if request.user.is_authenticated:
            return True
        return False


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity']
    search_fields = ['cart__user__username', 'product__name']

    def has_add_permission(self, request):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False

    def has_change_permission(self, request, _: CartItem | None = None):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False

    def has_delete_permission(self, request, _: CartItem | None = None):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False

    def has_view_permission(self, request, _: CartItem | None = None):
        if request.user.is_authenticated:
            return True
        return False


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'createdDate']
    search_fields = ['user__username', 'order_items__name', 'createdDate']

    def has_add_permission(self, request):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False

    def has_change_permission(self, request, _: Order | None = None):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False

    def has_delete_permission(self, request, _: Order | None = None):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False

    def has_view_permission(self, request, _: Order | None = None):
        if request.user.is_authenticated:
            return True
        return False


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity']
    search_fields = ['order__user__username', 'product__name']

    def has_add_permission(self, request):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False

    def has_change_permission(self, request, _: OrderItem | None = None):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False

    def has_delete_permission(self, request, _: OrderItem | None = None):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False

    def has_view_permission(self, request, _: OrderItem | None = None):
        if request.user.is_authenticated:
            return True
        return False


class DeliveryInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'city']
    search_fields = ['user__username', 'first_name', 'city']

    def has_add_permission(self, request):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False

    def has_change_permission(self, request, _: DeliveryInfo | None = None):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False

    def has_delete_permission(self, request, _: DeliveryInfo | None = None):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False

    def has_view_permission(self, request, _: DeliveryInfo | None = None):
        if request.user.is_authenticated:
            return True
        return False


admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(DeliveryInfo, DeliveryInfoAdmin)
