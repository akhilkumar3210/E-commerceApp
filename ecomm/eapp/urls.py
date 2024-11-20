from django.urls import path
from . import views
urlpatterns=[
    path('',views.ecom_login),
     path('logout',views.ecom_logout),
#----------------Admin----------------------------------------------------------------------
    path('shop_home',views.shop_home),
    path('product',views.add_product),
    path('edit/<id>',views.edit_product),
    path('delete/<pid>',views.delete_product),
    
#----------------User----------------------------------------------------------------------

    path('register',views.register),
    path('user_home',views.user_home),
    path('logout',views.user_logout),
    path('view/<pid>',views.view_product),
    path('addtocart/<pid>',views.add_to_cart),
    path('view_cart',views.view_cart),
    path('qty_sub/<cid>',views.qty_sub),
    path('qty_add/<cid>',views.qty_add),
    path('buy/<pid>',views.buy_product),
    path('bookings',views.user_bookings),
    
    
        
]