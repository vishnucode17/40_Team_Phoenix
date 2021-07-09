from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Product
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponse
# Create your views here.
def home(request):
    return render(request,'index.html')
def about(request):
    return render(request,'aboutus.html')

@login_required
def add_product(request):
    username = request.user.username
    email = request.user.email
    if request.method == 'POST':
        category = request.POST.get('category')
        product_name=request.POST.get('productName')
        product_description=request.POST.get('productDescription')
        mrp=request.POST.get('mrp')
        price=request.POST.get('price')
        slug=request.POST.get('slug')
        available=request.POST.get('pincodes')
        img_file = request.FILES['product_img']
        fs = FileSystemStorage()
        filename = fs.save(img_file.name,img_file)
        user = User.objects.get(username=request.user.username)
        new_product=Product.objects.create(product_name=product_name,category=category,product_description=product_description,date_added=timezone.now(),mrp=mrp,price=price,product_image=img_file,storename=user,slug=slug)
        new_product.save()
        return HttpResponse("Product added successfully!")
    return render(request,'add_product.html',{username:request.user.username,email:request.user.email})