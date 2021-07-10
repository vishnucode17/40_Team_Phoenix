from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product,OrderItem,Order
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponse
from textblob import TextBlob as tb
# Create your views here.
def home(request):
    return render(request,'home.html')
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

def search(request):
    print('abcd')
    product=request.GET['product']
    result=Product.objects.all().filter(product_name__icontains=product)
    result_len=len(result)
    if result_len==0:
        result=Product.objects.all().filter(category__icontains=product)
    result_len=len(result)
    search_string_length=len(result)>0
    product_details_search=[]
    if search_string_length:
        for i in range(len(result)):
            MRP=int(result[i].mrp.replace(',',''))
            result_price=int(result[i].price.replace(',',''))
            discount=100-round((result_price/MRP)*100)
            product_details_search.append((result[i].product_image.url,result[i],result[i].price,MRP,discount,result[i].slug))
    pars={'result':result,
        'product_details_search':product_details_search, 
        'search_string_length':search_string_length,
        'result_len':result_len,
        'product':product,}
    return render(request,'search.html',pars)

def product_view(request,slug):
    try:
        product = Product.objects.get(slug=slug)
        MRP=int(product.mrp.replace(',',''))
        result_price=int(product.price.replace(',',''))
        discount=100-round((result_price/MRP)*100)
        pars={
            'store':product.storename,
            'product_name':product.product_name,
            'category':product.category,
            'first_available':product.date_added,
            'mrp':product.mrp,
            'price':product.price,
            'product_img':product.product_image,
            'product_desc':product.product_description,
            'off':discount
        }
    except:
        print("Not found")
    return render(request,'product_view.html',pars)

def add_to_cart(request,slug):
    item=get_object_or_404(Product, slug=slug)
    order_item,created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_query = Order.objects.filter(user=request.user,ordered=False)
    if order_query.exists():
        order=order_query[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity+=1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        ordered_date=timezone.now()
        order=Order.objects.create(
            user=request.user,ordered_date=ordered_date
        )
        order.items.add(order_item)
    return redirect ('core:product_view',slug=slug)