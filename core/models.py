from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class Customer(models.Model):
    user=models.OneToOneField(User,null=False,blank=False,on_delete=models.CASCADE)
    mobile=models.BigIntegerField(null=False)
    def __str__(self):
        return self.user.username
class  Category(models.Model):
    category=models.CharField(max_length=30)
    def __str__(self):
        return self.category
class Product(models.Model):
    product_name=models.CharField(null=False,blank=False,max_length=32)
    product_category=models.ForeignKey('Category',on_delete=models.CASCADE)
    price=models.IntegerField(null=True)
    description=models.TextField()
    product_quantity=models.IntegerField(default=1)
    product_image=models.ImageField(null=True,upload_to='image/')
    def __str__(self):
        return self.product_name
class Image(models.Model):
    image_user=models.ForeignKey(Product,on_delete=models.CASCADE)
    photos=models.ImageField(upload_to='image/',null=True,blank=True )
class Order_items_models(models.Model):
    order_user=models.ForeignKey(User,on_delete=models.CASCADE)
    ordered_item_checkbox=models.BooleanField(default=False)
    order_product=models.ForeignKey(Product,on_delete=models.CASCADE)
    order_quantity=models.IntegerField(default=1)
    def __str__(self):
        return f"{self.order_product.product_name} of {self.order_quantity}"
    def get_total_item_price(self):
        return self.order_product.price * self.order_quantity
    def final_price(self):
        return self.get_total_item_price()
    
class Orders_list_model(models.Model):
    order_list_user=models.ForeignKey(User,on_delete=models.CASCADE)
    order_list_items=models.ManyToManyField(Order_items_models)
    order_list_start_time=models.DateTimeField(auto_now_add=True)
    order_list_ordered_checkbox=models.BooleanField(default=False)
    order_list_order_id=models.CharField(unique=True,null=True,blank=True,max_length=100)
    date_of_payment=models.DateTimeField(auto_now_add=True)
    order_delivered=models.BooleanField(default=False)
    order_received=models.BooleanField(default=False)
    order_razorpay_id=models.CharField(max_length=500,null=True,blank=True)
    order_payment_id=models.CharField(max_length=500,null=True,blank=True)
    order_signature_id=models.CharField(max_length=500,null=True,blank=True)

    def save(self,*args,**kwargs):
        if self.order_list_order_id is None and self.date_of_payment and self.id:
            self.order_list_order_id=self.date_of_payment.strftime('PAYME%Y%m%dord')+ str(self.id)
        return super().save(*args,**kwargs)
    def __str__(self):
        return self.order_list_user.username
    def get_total_product_items(self):
        total=0
        for item_list in self.order_list_items.all():
            total+= item_list.final_price()
        return total
    def total_orders(self):
        orders=Orders_list_model.objects.get(pk=self.pk)
        return orders.items.count()
    
class Check_out_model(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    country=CountryField(multiple=False,null=True,blank=True)
    first_name=models.CharField(max_length=13,null=True,blank=True)
    last_name=models.CharField(max_length=13,null=True,blank=True)
    company_name=models.CharField(max_length=30,null=True,blank=True,default=None)
    address=models.TextField(null=True,max_length=35,blank=True)
    state=models.CharField(max_length=20,null=True,blank=True)
    post_code=models.CharField(max_length=8,blank=True,null=True)
    order_note=models.TextField(max_length=300,null=True,blank=True)
    def __str__(self):
        return self.user.username

