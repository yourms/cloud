from django.http      import JsonResponse
from django.shortcuts import render, redirect
import os
from .models          import *
from django.core import serializers
from itertools import *
from django.db import connection
import json


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
    now_position = def_now_position()                      # 나중에 DB에서 긁어올것임
    route, route_list = def_route(now_position)            # 경로, 거처야할곳(상품 옆)
    camera_url = ['C:/Users/yourm/Desktop/yunghab3/me.jpg']
    # camera_url = ['https://cdn.top-rider.com/news/photo/202109/61445_132600_2439.jpg']
    context = {
        'map': martmap,                 # row, col 등
        'now_position':now_position,    # 현위치
        'route':route,                  # 거처야할곳
        'route_list':route_list,         # 경로
        'camera_url': camera_url,
    }
    if (typeMap == 'update'):
        return JsonResponse(context, safe=False)
        #return render(request, 'index.html', context)
    else:
        return render(request, 'index.html', context)

def def_now_position():
    now_position = "K_1"
    return now_position
'''
def mysql_query(query):  # 안씀.....
    try:
        cursor = connection.cursor()
        result = cursor.execute(query)
        select_result = cursor.fetchall()

        connection.commit()
        connection.close()

    except:
        connection.rollback()
        print("Failed Selecting")
    return result
'''
def rout_list_set(route_list):
    route_list2 = []
    for route in route_list:
        route2 = route.split("_")
        if(route2[1] in ["2","5","8","11"]):
            route2[1] = str(int(route2[1])-1)
            route = route2[0] + "_" + route2[1]
        if (route2[1] in ["3", "6", "9", "12"]):
            route2[1] = str(int(route2[1]) + 1)
            route = route2[0] + "_" + route2[1]
        route_list2.append(route)
    return route_list2

def def_route(now_position):
    print(">>>>  def_route")

    route_list = ["D_3", "E_8", "I_12"]  # 상품위치 나중에 DB에서 긁어와야함
    # route_list = ["D_3", "E_8", "I_12", "I_2", "J_3", "H_11"]    # 상품위치 나중에 DB에서 긁어와야함
    #route_list = ["I_2"]  # 상품위치 나중에 DB에서 긁어와야함
    route_list = rout_list_set(route_list) # 상품옆으로 변경
    route_list_copy = route_list.copy()
    route_list_copy.insert(0, now_position)         # 시작위치 끝 위치 추가하여 나중에 경로와 함께 리턴시킴
    route_list_copy.insert(len(route_list_copy), "A_1")

    # print(len(route_list))
    route_list = list(permutations(route_list, len(route_list))) # 경우의수 리스트
    shortest_route = []
    shortest_cnt = 0
    for route in route_list:
        route = list(route)
        route.insert(0, now_position) # 경우의수 전체에 시작위치 끝위치 추가
        route.insert(len(route), "A_1")
        # print(route)
        found_junction_list = []
        found_junction_cnt = 0
        print("route : ", route)
        for idx in range(0, len(route) - 1, 1):
            path = []
            # print("route[idx], route[idx + 1] : ", route[idx], route[idx + 1])
            # A-B-C-D 라면 A-B의 경로 B-C의 경로 C-D 의 경로 추가
            found_junction = find_junction(route[idx], route[idx + 1])
            # print("found_junction : ", found_junction)
            found_junction_list.append(found_junction)
            cnt = 0
            for fj in found_junction:
                cnt += (len(fj) - 1)
            found_junction_cnt += cnt
        print("***************************")
        print("found_junction_list : ", found_junction_list)
        print("found_junction_cnt : ", found_junction_cnt)
        print("***************************")
        # 가장짧은 경로로 덮어씀
        if (shortest_cnt > found_junction_cnt) or shortest_cnt == 0:
            shortest_route = found_junction_list
            shortest_cnt = found_junction_cnt
    print("##############")
    print("##############")
    print("##############")
    print("shortest_cnt : ", shortest_cnt)
    print("shortest_route : ", shortest_route)
    print("##############")
    print("##############")
    print("##############")
    print("route_list_copy : ", route_list_copy)
    s_route_list = []
    for s_items in shortest_route:
        for s_item in s_items:
            # print("s_item : ", s_item)
            s_route_list.append(s_item)

    return s_route_list, route_list_copy

# 부분 경로 반휜하는 find_junction
def find_junction(first, second):

    #print("first, second : ", first, second)
    junction = MartMap.objects.filter(junction=1)  # 모델에서 분기점 긁어옴
    junction = serializers.serialize('json', list(junction))
    junction = json.loads(junction)
    junction_list = []
    for i in junction:
        # print("fields : ", i['fields'])
        # print("fields.row : ", i['fields']['row'])
        junction_list.append(i['fields']['row'] + '_' + i['fields']['col'])

    # print(" junction[1]", junction[1].fields)
    #print("junction_list : ", junction_list)
    #junction_list = ['A_1','A_4','A_7','A_10','A_13','F_1','F_4','F_7','F_10','F_13','K_1','K_4','K_7','K_10','K_13']
    #first = "G_13"
    f_arr = first.split("_")
    #second = "J_1"
    s_arr = second.split("_")
    first_col = []
    second_col = []
    return_col_list = []
    if (f_arr[0] == s_arr[0]):
        return_col_list = [[first, second]]
    elif (f_arr[1] == s_arr[1]):
        return_col_list = [[first, second]]

    else:
        # if ((f_arr[0] == s_arr[0]) and (f_arr[0] in ['A','F','K']) ):
        #     pass
        # elif ((f_arr[1] == s_arr[1]) and (f_arr[1] in ['1','4','7','10','13']) ):
        #     pass
        #elif(f_arr[0] in ['A','F','K']):
        if(f_arr[0] in ['A', 'F', 'K']):
            first_col = [junction for junction in junction_list if (f_arr[0] == junction.split("_")[0])]
            if(s_arr[0] in ['A','F','K']):
                second_col = [junction for junction in junction_list if (s_arr[0] == junction.split("_")[0])]
            else:
                second_col = [junction for junction in junction_list if (s_arr[1] == junction.split("_")[1])]
        elif(f_arr[1] in ['1','4','7','10','13']):
            first_col = [junction for junction in junction_list if (f_arr[1] == junction.split("_")[1])]
            if (s_arr[0] in ['A', 'F', 'K']):
                second_col = [junction for junction in junction_list if (s_arr[0] == junction.split("_")[0])]
            else:
                second_col = [junction for junction in junction_list if (s_arr[1] == junction.split("_")[1])]

        else:
            pass
            #f_arr[1]
            # first_col = [junction  for junction in junction_list if (f_arr[0] == junction.split("_")[0] or f_arr[1] == junction.split("_")[1])]
            # second_col = [junction for junction in junction_list if (s_arr[0] == junction.split("_")[0] or s_arr[1] == junction.split("_")[1])]
            # inter_col = list(set(first_col).intersection(second_col))
            # print(inter_col)
        print("first_col, second_col : ", first_col, second_col)

        for f in first_col:
            f_0 = f.split("_")[0]
            f_1 = f.split("_")[1]
            for s in second_col:
                s_0 = s.split("_")[0]
                s_1 = s.split("_")[1]
                if (f_0 == s_0 and f != s):
                    return_col_list.append([f, s])
                if (f_1 == s_1 and f != s):
                    return_col_list.append([f, s])
    print("return_col_list : ", return_col_list)
    short_list = []
    short_len = 0
    for p in return_col_list:
        #print("p1 : ", p)
        p.insert(0, first)
        #print("p : ", p)
        #print("p-len : ", len(p))
        p.insert(len(p), second)
        #print("p2 : ", p)
        #print("p : ", p)
        p_list = []
        p_list_cnt = 0
        for idx in range(0, len(p)-1, 1):
            #print("p[idx], p[idx + 1] : ", p[idx], p[idx + 1])
            re_m_route = middle_route(p[idx], p[idx + 1])
            #print("re_m_route : ", re_m_route)
            if(re_m_route != []):
                p_list.append(re_m_route)
                p_list_cnt += (len(re_m_route) - 1)
        #print("p_list : ", p_list)
        #print("p_list_cnt : ", p_list_cnt)
        if(short_len > p_list_cnt ) or short_len == 0:
            short_list = p_list
            short_len = p_list_cnt
    #print("short_list : ", short_list)
    #print("short_len : ", short_len)
    return short_list

# 부분경로의 부분경로(이어지는셀 모두 반환)
def middle_route(first_position, second_position):
    #print(">>>>  def_route")
    #first_position = "A_1"
    f_arr = first_position.split("_")
    #second_position = "D_1"
    s_arr = second_position.split("_")
    return_list = []
    if(first_position == second_position):
        pass
    elif (f_arr[0] == s_arr[0]):
        if ((int(f_arr[1]) - int(s_arr[1])) <= 0):
            return_list = list(range(int(f_arr[1]), int(s_arr[1]) + 1, 1))
            #print("return_list : ", return_list)
        elif ((int(f_arr[1]) - int(s_arr[1])) > 0):
            #print(range(int(f_arr[1]), int(s_arr[1]) - 1, -1))
            return_list = list(range(int(f_arr[1]), int(s_arr[1]) - 1, -1))
        return_list = [ f_arr[0] + '_' +str(row) for row in return_list]
        #print("return_list2 : ", return_list)
    elif (f_arr[1] == s_arr[1]):
        if ( f_arr[0] > s_arr[0] ):
            return_list = list(map(chr, range(ord(f_arr[0]), ord(s_arr[0]) - 1, -1) ))

        elif ( f_arr[0] < s_arr[0] ):

            return_list = list(map(chr, range(ord(f_arr[0]), ord(s_arr[0]) + 1, 1) ))
        #print(return_list)
        return_list = [ col + '_' +f_arr[1] for col in return_list]
    # print("return_list : ", return_list)
    return return_list


