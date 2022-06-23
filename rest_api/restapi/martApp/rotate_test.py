import numpy as np

lists_arr = []
sound_lists = []
# Character range function
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
    global sound_lists
    result_first = np.where(lists_arr == first)
    result_second = np.where(lists_arr == second)
    if(result_first[0] > result_second[0]):
        print("전진")
        sound_lists.append("전진")
    elif(result_first[0] < result_second[0]):
        lists_arr = np.rot90(lists_arr, 2)
        #print(lists_arr)
        print("유턴")
        sound_lists.append("유턴")
    elif(result_first[1] > result_second[1]):
        lists_arr = np.rot90(lists_arr, -1)
        #print(lists_arr)
        print("좌회전")
        sound_lists.append("좌회전")
    elif(result_first[1] < result_second[1]):
        lists_arr = np.rot90(lists_arr, 1)
        #print(lists_arr)
        print("우회전")
        sound_lists.append("우회전")
def find_product(first, second):
    global lists_arr
    global sound_lists
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



def guide_mart(route_str):
    make_arr()
    for idx in range(0, len(route_str) - 1, 1):
        print(route_str[idx], route_str[idx + 1])
        rotate(route_str[idx], route_str[idx + 1])
        if idx == (len(route_str) -2):
            print(route_str[idx + 1])
            find_product(route_str[idx + 1], "G_9")

route_str = ['K_1','K_2','K_3','K_4','J_4', 'F_4', 'B_4', 'A_4', 'A_5', 'A_6', 'A_7', 'B_7', 'E_7', 'F_7', 'F_8', 'F_9', 'F_10', 'G_10']
guide_mart(route_str)

