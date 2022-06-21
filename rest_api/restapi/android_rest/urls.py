from django.urls import path,include
from android_rest.views import lists, loginandroid, goodsAndorid, searchProduct, searchProductCount, infoproduct, \
    writeList, writeUser, searchPrice, searchManufacture
from django.contrib import admin

urlpatterns = [
    path('lists', lists, name="lists"),
    path('loginandroid', loginandroid, name="loginandroid"),
    path('admin/', admin.site.urls),
    path('', include('helpweb.urls')),
    path('goodsandorid', goodsAndorid, name="goodsandroid"),
    path('searchProduct', searchProduct, name="searchProduct"),
    path('searchprice', searchPrice, name="searchprice"),
    path('searchManufacture', searchManufacture, name="searchManufacture"),
    path('searchcount', searchProductCount),
    path('infoproduct', infoproduct, name="infoproduct"),
    path('writeList', writeList, name="writeList"),
    path('writeUser', writeUser, name="writeUser")
    ]

