from django.contrib import admin
from .models import Seller
# Register your models here.
class SellerAdmin(admin.ModelAdmin):
    list_display=('name',)
    def active(self, obj): 
        return obj.is_active == 1
admin.site.register(Seller, SellerAdmin)