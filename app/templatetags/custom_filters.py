from django import template

register = template.Library()

@register.filter
def calculate_total(order_item):
    return order_item.product.price * order_item.quantity
