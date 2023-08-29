from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import UserInfo, Product, Category, Cart, CartItem, Order, OrderItem, DeliveryInfo
from .forms import RegistrationForm, LoginForm, CheckoutForm, CardPaymentForm
from django.contrib.auth import authenticate, login, logout
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum
from django.db import transaction


# Create your views here.


def index(request):
    categories = Category.objects.all()

    recent_products = Product.objects.all().order_by('-createdDate')[:4]
    context = {"categories": categories, "recent_products": recent_products}
    return render(request, "index.html", context)


def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = RegistrationForm()
    context = {"form": form}
    return render(request, "register.html", context)


def login_page(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = LoginForm()
    context = {"form": form, "username": request.user.username}
    return render(request, "login.html", context)


def logout_view(request):
    logout(request)
    return redirect(reverse('index'))


def products(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    five_days_ago = timezone.now() - timedelta(days=5)

    recent_products = Product.objects.order_by("-createdDate")
    sort_by = request.GET.get('sort_by', 'default')

    if sort_by == 'price_high':
        products = products.order_by('-price')
        recent_products = recent_products.order_by('-price')
    elif sort_by == 'price_low':
        products = products.order_by('price')
        recent_products = recent_products.order_by('price')
    elif sort_by == 'newest':
        products = products.order_by('-createdDate')
        recent_products = recent_products.order_by('-createdDate')
    elif sort_by == 'oldest':
        products = products.order_by('createdDate')
        recent_products = recent_products.order_by('createdDate')
    elif sort_by == 'name':
        products = products.order_by('name')
        recent_products = recent_products.order_by('name')

    context = {"categories": categories, "recent_products": recent_products, "products": products, "selected_sort": sort_by}
    return render(request, "products.html", context)


def product(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {"product": product}
    return render(request, "product.html", context)


def cart(request):
    cart = Cart.objects.get_or_create(user=request.user)[0]
    cart_items = cart.cartitem_set.select_related('product')

    order = Order.objects.filter(user=request.user).first()
    order_items = order.orderitem_set.select_related('product') if order else []

    context = {
        "cart": cart,
        "cart_items": cart_items,
        "order": order,
        "order_items": order_items,
    }
    return render(request, "cart.html", context)


def add_to_cart(request, product_id):
    if request.method == 'POST':
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product = Product.objects.get(id=product_id)

        # Get the quantity from the POST request data
        quantity = int(request.POST.get('quantity'))  # Default to 1 if quantity is not provided

        # Check if the product is already in the cart
        cart_item, created_cart_item = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created_cart_item:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item.quantity = quantity  # Set the quantity for newly created cart item
            cart_item.save()

    return redirect(reverse('index'))


def remove_from_cart(request, product_id):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    product = Product.objects.get(id=product_id)

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()  # Delete the cart item
    except CartItem.DoesNotExist:
        pass  # The item wasn't in the cart, do nothing

    return redirect("cart")


def update_cart(request):
    if request.method == 'POST':
        cart, _ = Cart.objects.get_or_create(user=request.user)

        for item in cart.cartitem_set.all():
            new_quantity = int(request.POST.get(f'quantity_{item.product.id}'))
            if new_quantity <= 0:
                item.delete()  # Remove the item from the cart
            else:
                item.quantity = new_quantity
                item.save()  # Update the quantity

    return redirect("cart")


def checkout(request):
    cart = Cart.objects.get_or_create(user=request.user)[0]
    cart_items = cart.cartitem_set.select_related('product')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            selected_payment_method = request.POST.get('payment_method')
            with transaction.atomic():
                existing_delivery_info = DeliveryInfo.objects.filter(
                    user=request.user,
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'],
                    address=form.cleaned_data['address'],
                    country=form.cleaned_data['country'],
                    city=form.cleaned_data['city'],
                    phone_number=form.cleaned_data['phone_number'],
                ).first()

                if existing_delivery_info:
                    delivery_info = existing_delivery_info
                else:
                    # Create and save delivery info
                    delivery_info = form.save(commit=False)
                    delivery_info.user = request.user
                    delivery_info.save()

                order, created = Order.objects.get_or_create(user=request.user)

                # Create order items if not created before
                if created:
                    for item in cart_items:
                        order_item, _ = OrderItem.objects.get_or_create(order=order, product=item.product)
                        order_item.quantity = item.quantity
                        order_item.save()

            if selected_payment_method == 'card':
                return redirect('payment_card')  # Redirect to credit card payment form
            else:
                return redirect('order_confirmation')

    else:
        form = CheckoutForm()
    # Calculate total order cost
    order, created = Order.objects.get_or_create(user=request.user)
    for item in cart_items:
        if order.orderitem_set.filter(product=item.product, quantity=item.quantity).exists():
            pass
        else:
            order.orderitem_set.create(product=item.product, quantity=item.quantity)
    total = 0
    order_items = OrderItem.objects.filter(order=order)
    total_order_cost = sum(item.quantity * item.product.price for item in order_items)
    total = total_order_cost + order.delivery_fee
    context = {
        "cart": cart,
        "cart_items": cart_items,
        "form": form,
        "order_items": order.orderitem_set.select_related('product'),
        "total_order_cost": total_order_cost,
        "total": total,
    }
    return render(request, "checkout.html", context)


def orders(request):
    orders = Order.objects.all()
    order_items = OrderItem.objects.all()
    context = {"orders": orders, "order_items": order_items}
    return render(request, "orders.html", context)



def order_complete(request, order_id):
    order = Order.objects.get(id=order_id)
    try:
        order_items = OrderItem.objects.filter(order=order)
        for order_item in order_items:
            order_item.delete()
        order.delete()
    except OrderItem.DoesNotExist:
        pass
    return redirect('orders')


def payment_card(request):
    if request.method == 'POST':
        form = CardPaymentForm(request.POST)
        if form.is_valid():
            return redirect('order_confirmation')
    else:
        form = CardPaymentForm()

    return render(request, "payment_card.html", {"form": form})


def order_confirmation(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    cart_items.delete()

    return render(request, "order_confirmation.html")


def contact(request):
    return render(request, "contact.html")


def locations(request):
    return render(request, "locations.html")


def phone(request):
    return render(request, "phone.html")


def aboutus(request):
    return render(request, "aboutus.html")
