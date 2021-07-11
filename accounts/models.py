from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Seller(models.Model):
    name=models.OneToOneField(User,on_delete=models.CASCADE)
    is_seller=models.BooleanField(default=False)
    def __str__(self):
        return self.name.username