from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from android_rest.models import User, Product, List
from android_rest.serializers import UserSerializer, ProductSerializer, SearchSerializer, PriceSerializer, \
    ManufactureSerializer, ListSerializer


def lists(request):
    if request.method == 'GET':
        datalist = User.objects.all()
        serializer = UserSerializer(datalist, many=True)
        return JsonResponse(serializer.data, safe=False, json_dumps_params={'ensure_ascii': False})


def loginandroid(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        id = data["id"]
        print(id)
        obj = User.objects.get(id=id)
        print("------------------------=====")
        print(obj)
        if data["password"] == obj.password:
            return JsonResponse("ok", safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse("fail", safe=False, json_dumps_params={'ensure_ascii': False})


def goodsAndorid(request):
    if request.method == 'GET':
        datalist = Product.objects.all()
        serializer = ProductSerializer(datalist, many=True)
        return JsonResponse(serializer.data, safe=False, json_dumps_params={'ensure_ascii': False})


def searchProduct(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        productName = data["name"]
        productName = productName.replace(" ", "")
        print(productName)
        objs = Product.objects.filter(name__icontains=productName).values('name')
        serializer = SearchSerializer(objs, many=True)
        print(serializer.data)
        return JsonResponse(serializer.data, safe=False, json_dumps_params={'ensure_ascii':False})


def searchPrice(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        productName = data["name"]
        productName = productName.replace(" ", "")
        print(productName)
        objs = Product.objects.filter(name__icontains=productName).values('price')
        serializer = PriceSerializer(objs, many=True)
        print(serializer.data)
        return JsonResponse(serializer.data, safe=False, json_dumps_params={'ensure_ascii': False})


def searchManufacture(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        productName = data["name"]
        productName = productName.replace(" ", "")
        print(productName)
        objs = Product.objects.filter(name__icontains=productName).values('manufacture')
        serializer = ManufactureSerializer(objs, many=True)
        print(serializer.data)
        return JsonResponse(serializer.data, safe=False, json_dumps_params={'ensure_ascii':False})


def pictureName(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        productName = data["id"]
        productName = productName.replace(" ", "")
        print(productName)
        objs = Product.objects.filter(id=productName).values('name')
        serializer = SearchSerializer(objs, many=True)
        return JsonResponse(serializer.data, safe=False, json_dumps_params={'ensure_ascii': False})


def picturePrice(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        productName = data["id"]
        productName = productName.replace(" ", "")
        print(productName)
        objs = Product.objects.filter(id=productName).values('price')
        serializer = PriceSerializer(objs, many=True)
        print(serializer.data)
        return JsonResponse(serializer.data, safe=False, json_dumps_params={'ensure_ascii': False})


def searchProductCount(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        productName = data["name"]
        productName = productName.replace(" ", "")
        print(productName)
        objs = Product.objects.filter(name__icontains=productName).values('name')
        objscount = objs.count()
        print(objscount)
        return JsonResponse(objscount, safe=False, json_dumps_params={'ensure_ascii': False})


def pictureManufacture(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        productName = data["id"]
        productName = productName.replace(" ", "")
        print(productName)
        objs = Product.objects.filter(id=productName).values('manufacture')
        serializer = ManufactureSerializer(objs, many=True)
        print(serializer.data)
        return JsonResponse(serializer.data, safe=False, json_dumps_params={'ensure_ascii':False})


def infoproduct(request):
    if request.method == 'GET':
        datalist = Product.objects.distinct().all()
        serializer = ProductSerializer(datalist, many=True)
        return JsonResponse(serializer.data, safe=False, json_dumps_params={'ensure_ascii': False})


def writeList(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        android_id = data["sessionid"]
        productName = data["name"]
        productName = productName.replace(" ", "")
        android_id = android_id.replace(",", "")
        print(productName)
        print(android_id)
        objs = Product.objects.filter(name__icontains=productName).values('pno')
        obj = User.objects.filter(id=android_id).values('uno')
        List(uno=obj, pno=objs).save()
        return JsonResponse("ok", safe=False, json_dumps_params={'ensure_ascii': False})


def writeUser(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        android_id = data["id"]
        password = data["password"]
        name = data["name"]
        User(id=android_id, password=password, name=name).save()
        return JsonResponse("ok", safe=False, json_dumps_params={'ensure_ascii': False})


def guardList(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        list_num = data["lno"]
        print(list_num)
        objs = List.objects.raw(
            "SELECT * FROM list l LEFT JOIN product p ON l.pno = p.pno WHERE l.lno = {}".format(list_num))[0]
        print(objs.main)
        print(objs.main)
        return JsonResponse(objs.main, safe=False, json_dumps_params={"ensure_ascii": False})


def nextList(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        list_num = data["lno"]
        print(list_num)
        objs = Product.objects.filter(name__icontains=list_num).values('main')
        serializer = ListSerializer(objs, many=True)
        print(serializer.data)
        return JsonResponse(serializer.data, safe=False, json_dumps_params={'ensure_ascii':False})

import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from martApp.path_maker import path_maker

def path_maker(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user_id = data["user_id"]
        now_position = data["now_position"]
        path_maker(user_id, now_position)
        return JsonResponse("ok", safe=False, json_dumps_params={'ensure_ascii':False})
        return JsonResponse(serializer.data, safe=False, json_dumps_params={'ensure_ascii': False})


def delList(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        list_num = data["lno"]
        print(list_num)
        objs = List.objs.all()
        objs.delete()
        okay = "okay"
        return JsonResponse(okay, safe=False, json_dumps_params={'ensure_ascii': False})


def updatePrimaryCount(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        list_num = data["lno"]
        print(list_num)
        objs = List.objects.raw("ALTER TABLE list AUTO_INCREMENT=1;")
        return JsonResponse(objs.main, safe=False, json_dumps_params={"ensure_ascii": False})
