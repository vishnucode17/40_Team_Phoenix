from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product,OrderItem,Order
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings 
from django.core.mail import send_mail 
from accounts.models import Seller
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
            'off':discount,
            'slug':product.slug,
            'available':product.available,
            'isavailable':product.isavailable,
            'n_orders':product.n_orders,
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
            messages.info(request,"Item Quantity Updated")
        else:
            order.items.add(order_item)
    else:
        ordered_date=timezone.now()
        order=Order.objects.create(
            user=request.user,ordered_date=ordered_date
        )
        order.items.add(order_item)
        messages.info(request,"Added Successfully to the cart")
    return redirect ('/mycart',slug=slug)
def remove_from_cart(request,slug):
    
    item=get_object_or_404(Product, slug=slug)
    order_query=Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_query.exists():
        order=order_query[0]
        if order.items.filter(item__slug=slug).exists():
            order_item=OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request,"Item Removed from the cart")
        else:
            messages.info(request,"Item is not in the cart")
            return redirect("/mycart",slug=slug)
    else:
        messages.info(request,"You don't have an active order")
        return redirect("/mycart",slug=slug)
    return redirect("/mycart",slug=slug)

@login_required
def cart(request):
        total_cart_price=0
        total_cart_discount=0
        total_cart_amount_save=0
        total_mrp=0
        print(request.user)
        result_cart=()
        order_query=OrderItem.objects.filter(user=request.user,ordered=False)
        cart_item=order_query
        for i in order_query:
            product_query=Product.objects.filter(product_name=i.item)
            product_query=product_query[0]
            result_cart+=((i.quantity,product_query.product_name,product_query.product_image,product_query.mrp,product_query.price,product_query.slug),)
            total_cart_price+=int(i.total_price())
            total_cart_discount+=int(i.total_discount())
            total_cart_amount_save+=int(i.total_amount_save())
            total_mrp+=int(product_query.mrp)*i.quantity
        print(total_cart_price)
        pars={'result_cart':result_cart,
        'n':len(order_query),
        'total_price':total_cart_price,
        'total_discount':total_cart_discount,
        'total_amount_save':total_cart_amount_save,
        'total_mrp':total_mrp
        }
        return render(request,'cart.html',pars)

@login_required    
def order_summary(request):
    if request.method == 'POST':
        address_one=request.POST['address_one']
        address_two=request.POST['address_two']
        pincode=request.POST['pincode']
        address_three=request.POST['address_three']
        address_four=request.POST['address_four']
        address_five=request.POST['address_five']
        full_name=request.user.first_name + ' ' + request.user.last_name
        order_query=OrderItem.objects.filter(user=request.user,ordered=False)
        order=Order.objects.filter(user=request.user,ordered=False)
        print(order)
        order=order[0]
        order.ordered=True
        order.save()
        buyer_text=''
        for i in order_query:
            i.ordered = True
            i.save()
            product_query=Product.objects.filter(product_name=i.item)
            product_query=product_query[0]
            product_query.n_orders+=1
            product_query.save()
            product_query.available-=i.quantity
            if product_query.available<0:
                messages.info(request,"Stock Not available")
            else:
                product_query.save()
                seller_mail=User.objects.get(username=product_query.storename)
                
                buyer_text += f'{i.item}\nprice: \u20B9 {product_query.price}\nquantity:{i.quantity}\nSold By: {product_query.storename}\n'
                seller_subject = f'New Order received {i.item}'
                seller_message = f'Hi {request.user.username}, You got a new order. Order details:\n{i.item}\nprice: {product_query.price}\nHave a great day.Check the website for more details.Have a great day'
                email_from = settings.EMAIL_HOST_USER 
                recipient_list = [request.user.email, ] 
                send_mail(seller_subject,seller_message, email_from, [seller_mail.email])
            buyer_subject = 'Order Placed'
            buyer_message=f'Hi {request.user.first_name} {request.user.last_name}, Thank you for shopping in GroKart. Order details:\n'+buyer_text+'\nHave a great day'
            send_mail( buyer_subject, buyer_message, email_from, recipient_list ) 
            return redirect('/thankyou')   

    return render(request,'order_summary.html')

def sellerview(request):
    sellerstatus=Seller.objects.filter(name=request.user)
    if sellerstatus.is_seller:
        if request.method == 'GET':
            pass
        else:
            seller_result=()
            orders=Product.objects.filter(storename=request.user)
            for i in orders:
                seller_result+=((prders.price),)

@login_required
def thankyou(request):
    return render(request,'Thankyou.html')