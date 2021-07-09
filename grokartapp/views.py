from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'index.html')
def about(request):
    return render(request,'aboutus.html')
def add_product(request):
    return render(request,'add_product.html')