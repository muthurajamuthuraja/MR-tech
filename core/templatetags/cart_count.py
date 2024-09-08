from django import template
from core.models import Orders_list_model


register=template.Library()
@register.filter()
def cart_item_count(user):
    if user.is_authenticated:
        fetch_item=Orders_list_model.objects.filter(order_list_user=user,order_list_ordered_checkbox=False)
        if fetch_item.exclude():
            return fetch_item[0].order_list_items.count()
    return 0

