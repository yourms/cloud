from django.http import JsonResponse
from rest_framework.parsers import JSONParser

from android_rest.models import User, Product
from android_rest.serializers import UserSerializer, ProductSerializer


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

