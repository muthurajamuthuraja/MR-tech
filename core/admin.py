from django.contrib import admin
from core.models import *

# Register your models here.
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Orders_list_model)
admin.site.register(Order_items_models)
admin.site.register(Check_out_model)
admin.site.register(Image)



