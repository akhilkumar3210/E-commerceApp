from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
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
            return redirect(ecom_login)
    else:
        return render(req,'login.html')

def ecom_logout(req):
    logout(req)
    return redirect(ecom_login)

#----------------Admin----------------------------------------------------------------------
def shop_home(req):
    return render(req,'shop/home.html')

#----------------User----------------------------------------------------------------------
