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
    user_id = "안녕"

    route, s_route_list_one_row, route_list, route_list_ori, sound_lists = def_route(now_position, user_id)            # 경로, 거처야할곳(상품 옆)
    #camera_list = os.listdir("../\static\images\trainimage\")
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
import numpy as np



import pymysql
#필요한 기본 DB 정보
host = "group3database.crjcswb8nh4o.us-west-1.rds.amazonaws.com" #접속할 db의 host명
user = "group3" #접속할 db의 user명
pw = "group3" #접속할 db의 password
db = "group3_db" #접속할 db의 table명 (실제 데이터가 추출되는 table)


def def_now_position():
    now_position = "K_1"
    return now_position

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


def def_route(now_position, user_id):
    print(">>>>  def_route")

    conn = pymysql.connect(host=host, user=user, password=pw, db=db)
    curs = conn.cursor()

    strSql = "select u.uno, l.lno, p.pno, p.name, p.location"
    strSql += " from user u"
    strSql += " left join list l on u.uno = l.uno"
    strSql += " left join product p on p.pno = l.pno"
    strSql += " where u.id = (%s)"
    curs.execute(strSql,(user_id))
    datas = curs.fetchall()
    route_list_ori_dataset = []
    for data in datas:
        row = {'uno': data[0],
               'lno': data[1],
               'pno': data[2],
               'name': data[3],
               'location': data[4], }

        route_list_ori_dataset.append(row)
    # print("route_list_ori_dataset : ", route_list_ori_dataset)
    # connection.commit()
    # connection.close()
    # db 접속 종료
    curs.close()
    conn.close()
    route_list_ori = []
    for i in route_list_ori_dataset:
        # print("fields : ", i['fields'])
        # print("fields.row : ", i['fields']['row'])
        # junction_list.append(i['fields']['row'] + '_' + i['fields']['col'])
        route_list_ori.append(i['location'])
    # print("route_list_ori : ", route_list_ori)
    # route_list_ori = ["D_3", "E_8", "I_12"]  # 상품위치 나중에 DB에서 긁어와야함
    route_list_ori_for_sound = route_list_ori.copy()
    # route_list = ["D_3", "E_8", "I_12", "I_2", "J_3", "H_11"]    # 상품위치 나중에 DB에서 긁어와야함
    #route_list = ["I_2"]  # 상품위치 나중에 DB에서 긁어와야함
    route_list = rout_list_set(route_list_ori) # 상품옆으로 변경
    route_list_for_sound = route_list.copy()
    route_list_copy = route_list.copy()
    route_list_copy.insert(0, now_position)         # 시작위치 끝 위치 추가하여 나중에 경로와 함께 리턴시킴
    route_list_copy.insert(len(route_list_copy), "A_1")

    route_list = list(permutations(route_list, len(route_list))) # 경우의수 리스트
    shortest_route = []
    shortest_cnt = 0
    for route in route_list:
        route = list(route)
        route.insert(0, now_position) # 경우의수 전체에 시작위치 끝위치 추가
        route.insert(len(route), "A_1")
        found_junction_list = []
        found_junction_cnt = 0
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
            s_route_list.append(s_item)
    s_route_list2 = s_route_list.copy()
    s_route_list3 = s_route_list.copy()
    sound_lists = guide_mart(s_route_list2, route_list_for_sound, route_list_ori_for_sound)
    sound_lists.append(" 계산대에 도착했습니다 안내를 마칩니다")
    s_route_list_one_row = []
    for idx, item in enumerate(s_route_list3):
        if(idx != 0):
            del item[0]
        s_route_list_one_row.extend(item);
    print("s_route_list : ", s_route_list)
    print("s_route_list_one_row : ", s_route_list_one_row)
    print("route_list_copy : ", route_list_copy)
    print("route_list_ori : ", route_list_ori)
    print("sound_lists : ", sound_lists)

    print("len(s_route_list_one_row) : ", len(s_route_list_one_row))
    print("len(sound_lists) : ", len(sound_lists))
    # s_route_list_one_row 와 sound_lists 의 짝수가 맞지않는다. 상품멈출후 물건담은담에 전진 하나가 더 써지기 때문이다.
    return s_route_list, s_route_list_one_row, route_list_copy, route_list_ori, sound_lists

# 부분 경로 반휜하는 find_junction
def find_junction(first, second):

    #junction = MartMap.objects.filter(junction=1)  # 모델에서 분기점 긁어옴
    # conn = pymysql.connect(host=host, user=user, password=pw, db=db)
    # curs = conn.cursor()
    #
    # strSql = "SELECT row, col, type, junction FROM MartMap WHERE junction = 1"
    # curs.execute(strSql)
    # datas = curs.fetchall()
    # junction = []
    # for data in datas:
    #     row = {'row': data[0],
    #            'col': data[1],
    #            'type': data[2],
    #            'junction': data[3],}
    #
    #     junction.append(row)
    #
    # #connection.commit()
    # #connection.close()
    # # db 접속 종료
    # curs.close()
    # conn.close()
    #print(junction)
    #junction = serializers.serialize('json', list(junction))
    #junction = json.loads(junction)
    junction_list = []
    # for i in junction:
    #     # print("fields : ", i['fields'])
    #     # print("fields.row : ", i['fields']['row'])
    #     #junction_list.append(i['fields']['row'] + '_' + i['fields']['col'])
    #     junction_list.append(i['row'] + '_' + i['col'])


    # print(" junction[1]", junction[1].fields)

    junction_list = ['A_1','A_4','A_7','A_10','A_13','F_1','F_4','F_7','F_10','F_13','K_1','K_4','K_7','K_10','K_13']
    # print("junction_list : ", junction_list)
    #first = "G_13"
    f_arr = first.split("_")
    #second = "J_1"
    s_arr = second.split("_")
    first_col = []
    second_col = []
    return_col_list = []
    if (f_arr[0] == s_arr[0] and (f_arr[0] in ['A', 'F', 'K'])):
        return_col_list = [[first, second]]
    elif (f_arr[1] == s_arr[1] and (f_arr[1] in ['1','4','7','10','13'])):
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

# A~K 까지 리스트만드는 함수
def range_char(start, stop):
    return (chr(n) for n in range(ord(start), ord(stop) + 1))

# 마트 맵을 Array로 만드는 함수
def make_arr():
    lists_arr = []
    for character in range_char("A", "K"):
        list_arr = []
        for number in range(1, 14, 1):
            list_arr.append(character + '_' + str(number))
        lists_arr.append(list_arr)
    lists_arr = np.asarray(lists_arr)
    return lists_arr

# 맵을 회전시킴 & 사운드스트링 append
def rotate(first, second, sound_lists, lists_arr):
    result_first = np.where(lists_arr == first) # 맵array에서 first의 value(ex A_1) 와 같은 값의 위치의 배열을 반환
    result_second = np.where(lists_arr == second)
    if(result_first[0] > result_second[0]):
        sound_lists.append("전진")
    elif(result_first[0] < result_second[0]):
        lists_arr = np.rot90(lists_arr, 2) # map array를 회전시킴
        sound_lists.append("유턴")
    elif(result_first[1] > result_second[1]):
        lists_arr = np.rot90(lists_arr, -1)
        sound_lists.append("좌회전")
    elif(result_first[1] < result_second[1]):
        lists_arr = np.rot90(lists_arr, 1)
        sound_lists.append("우회전")
    return sound_lists, lists_arr

# 상품을 찾았을때 사운드스트링 append
def find_product(first, second, sound_lists, lists_arr):
    result_first = np.where(lists_arr == first)
    result_second = np.where(lists_arr == second)
    if(result_first[0] > result_second[0]):
        print("정지 전방에 상품이 있습니다.")
        sound_lists.append("정지 전방에 상품이 있습니다")
    elif(result_first[0] < result_second[0]):
        print("정지 후방에 상품이 있습니다.")
        sound_lists.append("정지 후방에 상품이 있습니다")
    elif(result_first[1] > result_second[1]):
        print("정지 좌측에 상품이 있습니다.")
        sound_lists.append("정지 좌측에 상품이 있습니다")
    elif(result_first[1] < result_second[1]):
        print("정지 우측에 상품이 있습니다.")
        sound_lists.append("정지 우측에 상품이 있습니다")
    return sound_lists

# 사운드스트링 리스트 return
def guide_mart(route_arr, route_for_sound, route_list_ori_for_sound):
    print("#########   guide_mart    ##########")
    lists_arr = make_arr() # 나중에 길찾기 음성을 위해 마트맵을 array 형태로 그림
    sound_lists = []
    for index, route_str in enumerate(route_arr):
        for idx in range(0, len(route_str) - 1, 1):
            sound_lists, lists_arr = rotate(route_str[idx], route_str[idx + 1], sound_lists, lists_arr)
            if idx == (len(route_str) -2):
                if(route_str[idx + 1] in route_for_sound ):
                    route_str_list = []
                    route_str_list.append(route_str[idx + 1].split("_")[0] + "_" + str(int(route_str[idx + 1].split("_")[1]) - 1))
                    route_str_list.append(route_str[idx + 1].split("_")[0] + "_" + str(int(route_str[idx + 1].split("_")[1]) + 1))
                    for rsl in route_str_list:
                        if(rsl in route_list_ori_for_sound):
                            sound_lists = find_product(route_str[idx + 1], rsl, sound_lists, lists_arr)
                            route_list_ori_for_sound.remove(rsl)
    return sound_lists



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

lists_arr = [] # 나중에 길찾기 음성을 위해 마트맵을 array 형태로 그림
def def_route(now_position):
    print(">>>>  def_route")


    route_list_ori = ["D_3", "E_8", "I_12"]  # 상품위치 나중에 DB에서 긁어와야함
    # route_list = ["D_3", "E_8", "I_12", "I_2", "J_3", "H_11"]    # 상품위치 나중에 DB에서 긁어와야함
    #route_list = ["I_2"]  # 상품위치 나중에 DB에서 긁어와야함
    route_list = rout_list_set(route_list_ori) # 상품옆으로 변경
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
    route_str = ['K_1', 'K_2', 'K_3', 'K_4', 'J_4', 'F_4', 'B_4', 'A_4', 'A_5', 'A_6', 'A_7', 'B_7', 'E_7', 'F_7', 'F_8', 'F_9', 'F_10', 'G_10']
    guide_mart(route_str)

    return s_route_list, route_list_copy, route_list_ori

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

def range_char(start, stop):
    return (chr(n) for n in range(ord(start), ord(stop) + 1))

def make_arr():
    global lists_arr
    for character in range_char("A", "K"):
        list_arr = []
        for number in range(1, 14, 1):
            print(character + '_' + str(number))
            list_arr.append(character + '_' + str(number))
        lists_arr.append(list_arr)
    print(lists_arr)
    print(type(lists_arr))
    lists_arr = np.asarray(lists_arr)

def rotate(first, second):
    global lists_arr
    result_first = np.where(lists_arr == first)
    result_second = np.where(lists_arr == second)
    if(result_first[0] > result_second[0]):
        print("전진")
    elif(result_first[0] < result_second[0]):
        lists_arr = np.rot90(lists_arr, 2)
        #print(lists_arr)
        print("유턴")
    elif(result_first[1] > result_second[1]):
        lists_arr = np.rot90(lists_arr, -1)
        #print(lists_arr)
        print("좌회전")
    elif(result_first[1] < result_second[1]):
        lists_arr = np.rot90(lists_arr, 1)
        #print(lists_arr)
        print("우회전")
def find_product(first, second):
    global lists_arr
    result_first = np.where(lists_arr == first)
    result_second = np.where(lists_arr == second)
    if(result_first[0] > result_second[0]):
        print("정지 전방에 상품이 있습니다.")
    elif(result_first[0] < result_second[0]):
        print("정지 후방에 상품이 있습니다.")
    elif(result_first[1] > result_second[1]):
        print("정지 좌측에 상품이 있습니다.")
    elif(result_first[1] < result_second[1]):
        print("정지 우측에 상품이 있습니다.")



def guide_mart(route_str):
    make_arr()
    for idx in range(0, len(route_str) - 1, 1):
        print(route_str[idx], route_str[idx + 1])
        rotate(route_str[idx], route_str[idx + 1])
        if idx == (len(route_str) -2):
            print(route_str[idx + 1])
            find_product(route_str[idx + 1], "G_9")

'''
