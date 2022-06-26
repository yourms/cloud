from django.http      import JsonResponse
from django.shortcuts import render, redirect
import os
from .models          import *
from django.core import serializers
from itertools import *
from django.db import connection
import json


import pymysql
#필요한 기본 DB 정보
host = "group3database.crjcswb8nh4o.us-west-1.rds.amazonaws.com" #접속할 db의 host명
user = "group3" #접속할 db의 user명
pw = "group3" #접속할 db의 password
db = "group3_db" #접속할 db의 table명 (실제 데이터가 추출되는 table)


def index(request):
    print('>>>>web index')

    typeST = request.POST.get('typeST', '')  # 아직은 의미없음 나중에 수시로 update 할 경우 필요할수도 있을거 같아서 미리 적어놓음
    #list(map(chr, range(97, 123)))  # or list(map(chr, range(ord('a'), ord('z')+1)))
    rows = list(map(chr, range(ord('A'), ord('K')+1)))  # 초기 세팅 셀 tr, td 이름
    cols = list(range(1, 14, 1))                        # 초기 세팅 셀 tr, td 이름
    routes = list(range(0, 15, 1))                     # 초기 세팅 우측 테이블 갯수 미리 만들어 놓음

    context = {'rows': rows,
               'cols': cols,
               'routes': routes,

               }
    if (typeST == 'update'):
        return JsonResponse(context, safe=False)
    else:
        return render(request, 'index.html', context)

def updateMap(request):
    print(">>>> updateMap")
    typeMap = request.POST.get('typeMap', '')

    martmap = MartMap.objects.all().order_by('row','col')  # MartMap 에서 데이터 긁어옴(테이블 세팅 하기위해)
    martmap = serializers.serialize('json', list(martmap))
    # now_position = def_now_position()                      # 나중에 DB에서 긁어올것임
    user_id = "안녕"
    now_position = "K_1"
    camera_list = os.listdir("./martApp/static/images/trainimage/")
    camera_list = [filename.split(".")[0] for filename in camera_list]
    camera_list.sort(reverse=True)
    camera_url = camera_list
    # camera_url = ['https://cdn.top-rider.com/news/photo/202109/61445_132600_2439.jpg']

    conn = pymysql.connect(host=host, user=user, password=pw, db=db)
    curs = conn.cursor()

    strSql = "select list_path from path_list pl "
    strSql += " where user_id = (%s) "
    strSql += " and main_no = (select max(seq) from path_main pm where user_id = (%s))"
    curs.execute(strSql, (user_id, user_id))
    route_crud = curs.fetchall()
    #route = list(route)
    route_crud = list(map(list, route_crud))
    route = []
    for r in route_crud:
        r = r[0].split(",")
        route.append(r)

    strSql = "select path_one_row, route_str, p_location, sound_str from path_list_detail "
    strSql += " where user_id = (%s) "
    strSql += " and main_no = (select max(seq) from path_main pm where user_id = (%s))"
    curs.execute(strSql, (user_id, user_id))
    datas = curs.fetchall()
    path_one_row = []
    route_str = []
    p_location = []
    sound_str = []

    for data in datas:
        path_one_row = data[0]
        route_str = data[1]
        p_location = data[2]
        sound_str = data[3]
    path_one_row = path_one_row.split(",")
    route_str = route_str.split(",")
    p_location = p_location.split(",")
    sound_str = sound_str.split(",")

    context = {
        'map': martmap,                 # row, col 등
        'now_position':now_position,    # 현위치
        'route':route,                  # 거처야할곳
        'route_list':route_str,         # 경로
        'camera_url': camera_url,
        'route_list_ori': p_location,
        'sound_list' : sound_str,
    }
    if (typeMap == 'update'):
        return JsonResponse(context, safe=False)
        #return render(request, 'index.html', context)
    else:
        return render(request, 'index.html', context)
'''
def updateMap_back(request):
    print(">>>> updateMap")
    typeMap = request.POST.get('typeMap', '')

    martmap = MartMap.objects.all().order_by('row','col')  # MartMap 에서 데이터 긁어옴(테이블 세팅 하기위해)
    martmap = serializers.serialize('json', list(martmap))
    # now_position = def_now_position()                      # 나중에 DB에서 긁어올것임
    user_id = "안녕"
    now_position = "K_1"

    route, s_route_list_one_row, route_list, route_list_ori, sound_lists = def_route(now_position, user_id)            # 경로, 거처야할곳(상품 옆)
    camera_list = os.listdir("./martApp/static/images/trainimage/")
    camera_list = [filename.split(".")[0] for filename in camera_list]
    camera_list.sort(reverse=True)
    print("camera_list : ", camera_list)
    camera_url = camera_list
    # camera_url = ['https://cdn.top-rider.com/news/photo/202109/61445_132600_2439.jpg']
    context = {
        'map': martmap,                 # row, col 등
        'now_position':now_position,    # 현위치
        'route':route,                  # 거처야할곳
        'route_list':route_list,         # 경로
        'camera_url': camera_url,
        'route_list_ori': route_list_ori,
    }
    if (typeMap == 'update'):
        return JsonResponse(context, safe=False)
        #return render(request, 'index.html', context)
    else:
        return render(request, 'index.html', context)

'''