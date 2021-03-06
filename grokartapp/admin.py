from django.contrib import admin
from . models import Product,OrderItem,Order
from django.contrib.auth.models import User
# Register your models here.
class ProductAdmin(admin.ModelAdmin): 
    list_display = ('storename','product_name','category','date_added') 
    #search_fields = ("storename__startswith", )
    def active(self, obj): 
        return obj.is_active == 1
  
    active.boolean = True

class OrderItemAdmin(admin.ModelAdmin):
    list_display=('user',)
    def active(self, obj): 
        return obj.is_active == 1

class OrderAdmin(admin.ModelAdmin):
    list_display=('user',)
    def active(self, obj): 
        return obj.is_active == 1
admin.site.site_header = "GroKart Admin Portal"
admin.site.site_title = "GroKart Admin Portal"
admin.site.index_title = "Welcome to GroKart Admin"
admin.site.register(Product, ProductAdmin) 
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(Order, OrderAdmin)