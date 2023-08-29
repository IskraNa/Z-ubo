from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class UserInfo(models.Model):
    ROLE_CHOICES = (
        ('a', 'Admin'),
        ('r', 'Retailer'),
        ('c', 'Customer'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user}"


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.CharField(primary_key=True, max_length=50, blank=True, auto_created=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='products')
    price = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    width = models.CharField(max_length=255)
    height = models.CharField(max_length=255)
    quantityAvailable = models.IntegerField()
    image = models.ImageField(upload_to="products/")
    createdDate = models.DateField(auto_now_add=True)
    updatedDate = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="CartItem")
    createdDate = models.DateField(auto_now_add=True)
    updatedDate = models.DateField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def subtotal(self):
        return self.product.price * self.quantity


class DeliveryInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)


class Order(models.Model):
    PAYMENT_CHOICES = (
        ("cash", "Cash"),
        ("card", "Card")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_items = models.ManyToManyField(Product, through="OrderItem")
    delivery_info = models.ForeignKey(DeliveryInfo, on_delete=models.CASCADE, null=True)
    delivery_fee = models.IntegerField(default=120)
    payment_method = models.CharField(choices=PAYMENT_CHOICES, max_length=10, default="card")
    createdDate = models.DateField(auto_now_add=True)

    def subtotal(self):
        return sum(item.subtotal() for item in self.order_items.all())

    def total(self):
        total = self.subtotal() + self.delivery_fee
        return total

    def __str__(self):
        return f"Order for {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


