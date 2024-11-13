from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
# Create your views here.
def ecom_login(req):
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['password']
        shop=authenticate(username=uname,password=password)
        if shop:
            login(req,shop)
            return redirect(shop_home)
        else:
            messages.warning(req,'Invaild username or password!!!')
            return redirect(ecom_login)
    else:
        return render(req,'login.html')

def ecom_logout(req):
    logout(req)
    return redirect(ecom_login)

#----------------Admin----------------------------------------------------------------------
def shop_home(req):
    product=Product.objects.all()
    return render(req,'shop/home.html',{'products':product})

def add_product(req):
    return render(req,'shop/product.html')
#----------------User----------------------------------------------------------------------
