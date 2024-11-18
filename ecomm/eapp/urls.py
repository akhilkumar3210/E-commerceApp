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
    

    
]