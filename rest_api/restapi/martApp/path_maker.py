import numpy as np
from django.http      import JsonResponse
from django.shortcuts import render, redirect
#from .models          import *
from django.core import serializers
from itertools import *
from django.db import connection
import json
#pip install pymysql
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
def test_maker():
    print("test_maker !!!")

def path_maker(user_id, now_position):
    if(user_id == ""):
        user_id = "안녕"

    conn = pymysql.connect(host=host, user=user, password=pw, db=db)
    curs = conn.cursor()


    # now_position = def_now_position()
    s_route_list, s_route_list_one_row, route_list_copy, route_list_ori, sound_lists = def_route(now_position, user_id)

    sql_select = "select l_grp from list where uno = (select uno from user where id = (%s))"
    curs.execute(sql_select, (user_id))
    list_num = 0
    for row in curs.fetchall():
        list_num = row[0]
    print("list_num : ", list_num)

    print("user_id : ", user_id)
    # path_mainSql = "insert into path_main(user_id, list_num)"
    # path_mainSql += " values (?,?)"
    # curs.execute(path_mainSql, (user_id, list_num))
    curs.execute("insert into path_main (user_id, list_num)values (%s,%s)", (user_id, int(list_num) ))
    conn.commit()

    sql_select = "select  max(seq) from path_main where user_id = (%s) group by user_id"
    curs.execute(sql_select, (user_id))
    main_no = 0
    for row in curs.fetchall():
        main_no = row[0]
    path_list_insert = []
    for index, routes in enumerate(s_route_list):
        # print(type(routes))
        routes_str = ','.join(routes)
        path_list_insert.append([main_no,index+1,user_id,routes_str])

    path_listSql = "insert into path_list(main_no, list_no, user_id, list_path)"
    path_listSql += "values(%s,%s,%s,%s)"
    curs.executemany(path_listSql, path_list_insert)
    conn.commit()
    s_route_list_one_row_str = ','.join(s_route_list_one_row)
    route_list_copy_str = ','.join(route_list_copy)
    route_list_ori_str = ','.join(route_list_ori)
    sound_lists_str_str = ','.join(sound_lists)
    path_list_detailSql = "insert into path_list_detail(main_no, user_id, path_one_row, route_str, p_location, sound_str)"
    path_list_detailSql += "values(%s,%s,%s,%s,%s,%s)"
    curs.execute(path_list_detailSql, (main_no, user_id, s_route_list_one_row_str, route_list_copy_str, route_list_ori_str, sound_lists_str_str))
    conn.commit()


    # connection.commit()
    # connection.close()
    # db 접속 종료
    curs.close()
    conn.close()
path_maker("")




