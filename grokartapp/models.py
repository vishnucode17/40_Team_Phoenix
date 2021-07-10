from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
# Create your models here.
class Product(models.Model):
    storename = models.ForeignKey(User,on_delete=models.CASCADE)
    id=models.AutoField(primary_key=True)
    product_name=models.CharField(max_length=255)
    category=models.CharField(max_length=255)
    date_added=models.DateTimeField('first available',default=timezone.now())
    mrp=models.CharField(max_length=255)
    price=models.CharField(max_length=255)
    product_description=models.CharField(max_length=1024)
    slug = models.SlugField(max_length = 250, null = True, blank = True,unique = True)
    product_image=models.ImageField(upload_to='product_images')
    n_orders=models.IntegerField(default=0)
    rating=models.IntegerField(default=0)
    def __str__(self):
        return self.product_name
    def get_add_to_cart_url(self):
        return reverse('core:add-to-cart',kwargs={
            'slug':self.slug
        })

class OrderItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    def __str__(self):
        return f"{self.quantity} of {self.item.product_name}"
    def total_price(self):
        return self.quantity*int(self.item.price)
    def total_discount(self):
        return self.quantity * (self.item.mrp - self.item.price)
    def total_amount_save(self):
        return self.total_price()-self.total_discount()

class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    items=models.ManyToManyField(OrderItem)
    start_date=models.DateTimeField(auto_now_add=True)
    ordered_date=models.DateTimeField()
    ordered=models.BooleanField(default=False)
    def __str__(self):
        return self.user.username
    