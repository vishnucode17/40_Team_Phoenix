from django.contrib import admin
from . models import Product
from django.contrib.auth.models import User
# Register your models here.
class ProductAdmin(admin.ModelAdmin): 
    list_display = ('storename','product_name','category','date_added') 
    def active(self, obj): 
        return obj.is_active == 1
  
    active.boolean = True
  
admin.site.register(Product, ProductAdmin) 