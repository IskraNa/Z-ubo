"""
URL configuration for zubo_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from app import views

urlpatterns = [
        path('admin/', admin.site.urls),
        path('', views.index, name='index'),
        path('register/', views.register_page, name='register'),
        path('login/', views.login_page, name='login'),
        path('logout/', views.logout_view, name='logout'),
        path('products/', views.products, name='products'),
        path('product/<int:product_id>/', views.product, name='product'),
        path('shoppingCartAdd/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
        path('shoppingCart/', views.cart, name='cart'),
        path('shoppingCartRemove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
        path('shoppingCartUpdate/', views.update_cart, name='update_cart'),
        path('checkout/', views.checkout, name='checkout'),
        path('payment/card/', views.payment_card, name='payment_card'),
        path('order/confirmation/', views.order_confirmation, name='order_confirmation'),
        path('orders/', views.orders, name='orders'),
        path('order/complete/<int:order_id>/', views.order_complete, name='order_complete'),
        path('contact/', views.contact, name='contact'),
        path('locations/', views.locations, name='locations'),
        path('phone/', views.phone, name='phone'),
        path('aboutus/', views.aboutus, name='aboutus'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
