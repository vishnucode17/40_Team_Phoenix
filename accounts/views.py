from django.shortcuts import render
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import logout as Logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from grokartapp.models import Product,OrderItem
# Create your views here.
def login(request):
    if request.user.is_authenticated:
       return redirect('home') 
    else:
        if request.method =='POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.info(request,'Invalid Credentials')
                return redirect('/accounts/login')
        return render(request,'accounts/login.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method=='POST':
            username=request.POST.get('username')
            email=request.POST.get('email')
            first_name=request.POST.get('firstName')
            last_name=request.POST.get('lastName')
            password=request.POST.get('password')
            vpassword=request.POST.get('vpassword')
            if password==vpassword:
                if User.objects.filter(username=username).exists():
                    messages.info(request,'User already exists')
                    return redirect('/accounts/signup')
                else:
                    user=User.objects.create_user(username=username,email=email,first_name=first_name,last_name=last_name,password=password)
                    user.save()
                    return redirect('/accounts/login')
            else:
                messages.info(request,'Password Mismatch')
                return redirect('/accounts/signup')
        else:
            return render(request,'accounts/signup.html')

@login_required
def logout(request):
    Logout(request)
    return redirect('/')

def myaccount(request):
    user_name=request.user.username
    email=request.user.email
    result_cart=()
    order_query=OrderItem.objects.filter(user=request.user,ordered=True)
    print(order_query)
    for i in order_query:
            product_query=Product.objects.filter(product_name=i.item)
            product_query=product_query[0]
            result_cart+=((i.quantity,product_query.product_name,product_query.product_image,product_query.mrp,product_query.price,product_query.slug),)
    try:
        first_letter=request.user.first_name[0].upper()
    except:
        first_letter=""
    return render(request,'accounts/myaccount.html',{'profile_letter':first_letter,'result_cart':result_cart})