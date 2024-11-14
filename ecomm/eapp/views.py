from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
# Create your views here.
def ecom_login(req):
    if 'shop' in req.session:
        return redirect(shop_home)
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['password']
        shop=authenticate(username=uname,password=password)
        if shop:
            login(req,shop)
            req.session['shop']=uname   
            return redirect(shop_home)
        else:
            messages.warning(req,'Invaild username or password!!!')
            return redirect(ecom_login)
    else:
        return render(req,'login.html')

def ecom_logout(req):
    logout(req)
    req.session.flush()
    return redirect(ecom_login)

#----------------Admin----------------------------------------------------------------------
def shop_home(req):
    if 'shop' in req.session:
        product=Product.objects.all()
        return render(req,'shop/home.html',{'products':product})
    else:
        return redirect(ecom_login)
def add_product(req):
    if 'shop' in req.session:
        if req.method=='POST':
            pid=req.POST['p_id']
            name=req.POST['name']
            descri=req.POST['description']
            price=req.POST['p_price']
            o_price=req.POST['of_price']
            stock=req.POST['p_stock']
            img=req.FILES['p_img']
            data=Product.objects.create(pid=pid,name=name,descri=descri,price=price,off_price=o_price,stock=stock,img=img)
            data.save()
            return redirect(shop_home)
        else:        
            return render(req,'shop/product.html')
    else:
        return redirect(ecom_login)
def edit_product(req,id):
    if req.method=='POST':
        pid=req.POST['p_id']
        name=req.POST['name']
        descri=req.POST['description']
        price=req.POST['p_price']
        o_price=req.POST['of_price']
        stock=req.POST['p_stock']
        img=req.FILES.get('p_img')
        if img:
            Product.objects.filter(pk=id).update(pid=pid,name=name,descri=descri,price=price,off_price=o_price,stock=stock)
            data=Product.objects.get(pk=id)
            data.img=img
            data.save()
        else:
            Product.objects.filter(pk=id).update(pid=pid,name=name,descri=descri,price=price,off_price=o_price,stock=stock)
        return redirect(shop_home)
    else:
        data=Product.objects.get(pk=id)
        return render(req,'shop/edit.html',{'data':data})
#----------------User----------------------------------------------------------------------
