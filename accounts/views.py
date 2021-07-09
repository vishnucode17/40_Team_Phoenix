from django.shortcuts import render
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.shortcuts import redirect
# Create your views here.
def login(request):
    if request.method =='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('login')
    return render(request,'accounts/login.html')

def register(request):
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
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username,email=email,first_name=first_name,last_name=last_name,password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request,'Password Mismatch')
            return redirect('signup')
    else:
        return render(request,'accounts/signup.html')