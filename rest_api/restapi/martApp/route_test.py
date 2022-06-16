from itertools import *


def middle_route(first_position, second_position):
    #print(">>>>  def_route")
    #first_position = "A_1"
    f_arr = first_position.split("_")
    #second_position = "D_1"
    s_arr = second_position.split("_")
    return_list = []
    if (f_arr[0] == s_arr[0]):
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
    return return_list


def find_junction(first, second):

    #print("first, second : ", first, second)
    junction_list = ['A_1','A_4','A_7','A_10','A_13','F_1','F_4','F_7','F_10','F_13','K_1','K_4','K_7','K_10','K_13']
    #first = "G_13"
    f_arr = first.split("_")
    #second = "J_1"
    s_arr = second.split("_")
    first_col = []
    second_col = []
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
    #print("first_col, second_col : ", first_col, second_col)
    return_col_list  = []
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
    #print("return_col_list : ", return_col_list)
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

        #print([print(junction) for junction in junction_list])
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
route_list = ["D_3", "E_8", "I_12", "I_2"]
route_list = rout_list_set(route_list)
#print(len(route_list))
route_list = list(permutations(route_list, len(route_list)))
shortest_route = []
shortest_cnt = 0
for route in route_list:
    route = list(route)
    route.insert(0, "A_1")
    route.insert(len(route), "A_1")
    #print(route)
    found_junction_list = []
    found_junction_cnt = 0
    print("route : ", route)
    for idx in range(0, len(route) -1, 1):
        path = []

        #print("route[idx], route[idx + 1] : ", route[idx], route[idx + 1])
        found_junction = find_junction(route[idx], route[idx + 1])
        #print("found_junction : ", found_junction)
        found_junction_list.append(found_junction)
        cnt = 0
        for fj in found_junction:
            cnt += (len(fj) - 1)
        found_junction_cnt += cnt
    print("***************************")
    print("found_junction_list : ", found_junction_list)
    print("found_junction_cnt : ", found_junction_cnt)
    print("***************************")
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



