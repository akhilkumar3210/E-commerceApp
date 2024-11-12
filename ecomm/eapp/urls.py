from django.urls import path
from . import views
urlpatterns=[
    path('',views.ecom_login),
    path('shop_home',views.shop_home),
    path('logout',views.ecom_logout),
]