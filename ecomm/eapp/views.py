from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
import os
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def ecom_login(req):
    if 'shop' in req.session:
        return redirect(shop_home)
    if 'user' in req.session:
        return redirect(user_home)
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['password']
        shop=authenticate(username=uname,password=password)
        if shop:
            login(req,shop)
            if shop.is_superuser:
                req.session['shop']=uname   
                return redirect(shop_home)
            else:
                req.session['user']=uname   
                return redirect(user_home)
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
    
def delete_product(req,pid):
    data=Product.objects.get(pk=pid)
    file=data.img.url
    file=file.split('/')[-1]
    os.remove('media/'+file)
    data.delete()
    return redirect(shop_home)

#----------------User----------------------------------------------------------------------

def register(req):
    if req.method=='POST':
        email=req.POST['email']
        uname=req.POST['uname']
        password=req.POST['password']
        try:
            data=User.objects.create_user(first_name=uname,email=email,username=email,password=password)
            data.save()
            send_mail('Registration In EcommShop', 'Successfully Registered In EcommShop', settings.EMAIL_HOST_USER, [email])
            return redirect(ecom_login)
        except:
            messages.warning(req,'Email Already Exists!!')
            return redirect(register)
    else:
        return render(req,'user/register.html')
    
def user_home(req):
    if 'user' in req.session:
        product=Product.objects.all()
        return render(req,'user/user.html',{'products':product})

def user_logout(req):
    logout(req)
    req.session.flush()
    return redirect(ecom_login)

def view_product(req,pid):
    data=Product.objects.get(pk=pid)
    return render(req,'user/view_product.html',{'data':data})

def add_to_cart(req,pid):
    product=Product.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    try:
        cart=Cart.objects.get(product=product,user=user)
        cart.qty+=1
        cart.save()
    except:
        data=Cart.objects.create(product=product,user=user,qty=1)
        data.save()
    return redirect(view_cart)

def view_cart(req):
    user=User.objects.get(username=req.session['user'])
    data=Cart.objects.filter(user=user)
    return render(req,'user/cart.html',{'cart':data})

def qty_add(req,cid):
    data=Cart.objects.get(pk=cid)
    if data.product.stock > data.qty:
        data.qty+=1
        data.save()
    return redirect(view_cart)


def qty_sub(req,cid):
    data=Cart.objects.get(pk=cid)
    data.qty-=1
    data.save()
    if data.qty==0:
        data.delete()
    return redirect(view_cart)

def buy_product(req,pid):
    product=Product.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    qty=1
    price=product.off_price
    buy=Buy.objects.create(product=product,user=user,qty=qty,tot_price=price)
    buy.save()
    return redirect(user_bookings)

def cart_buy(req,cid):
    cart=Cart.objects.get(pk=cid)
    price=cart.qty*cart.product.off_price
    stock=cart.product.stock-cart.qty
    
    if stock==0:
        messages.warning(req,'Out of Stock!!!'+cart.product.name)
        return redirect(view_cart)
    buy=Buy.objects.create(product=cart.product,user=cart.user,qty=cart.qty,tot_price=price)
    buy.save()
    return redirect(user_bookings)

def user_bookings(req):
    user=User.objects.get(username=req.session['user'])
    bookings=Buy.objects.filter(user=user)[::-1]
    return render(req,'user/bookings.html',{'bookings':bookings})


def us_bookings(req):
    bookings=Buy.objects.all()[::-1]
    return render(req,'shop/ubookings.html',{'bookings':bookings})