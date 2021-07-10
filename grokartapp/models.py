from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
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
    slug = models.SlugField(max_length = 250, null = True, blank = True)
    product_image=models.ImageField(upload_to='product_images')
    def __str__(self):
        return self.product_name
