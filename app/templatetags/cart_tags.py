from django import template
from ..models import CartItem
register = template.Library()


@register.simple_tag
def cart_item_count(user):
    return CartItem.objects.filter(cart__user=user).count()