import collections
import random
from collections import OrderedDict
import pandas as pd
import operator
import openpyxl

data = pd.read_excel('list_4975.xlsx')

original_data = data
data = data.transpose()
data.rename(columns=data.iloc[0], inplace=True)
original_dict = data.to_dict('dict')
OrderedDict(original_dict)


def get_vol(dict):
    price = dict[1]['Market Cap']
    return price


original_dict = dict(sorted(original_dict.items(), key=get_vol, reverse=True))

def isFull(layer, capacity):
    if len(layer) >= capacity:
        return True
    else:
        return False


def decide_in_layer(key, layer):
    if key in layer:
        return True
    else:
        return False


# 목표로 하는 값의 인덱스 번호 찾기
def search(given_value, index_dict):
    for key, value in index_dict.items():
        if value == given_value:
            object_key = key
    return object_key


# search에서 찾은 인덱스 값을 바탕으로 같은 블록안에 있는 키들의 인덱스를 리스트로 모음
def key_list_func_for_L3(object_key):
    if object_key % 4 == 1:
        key_list = (object_key, object_key + 1, object_key + 2, object_key + 3)
    elif object_key % 4 == 2:
        key_list = (object_key - 1, object_key, object_key + 1, object_key + 2)
    elif object_key % 4 == 3:
        key_list = (object_key - 2, object_key - 1, object_key, object_key + 1)
    elif object_key % 4 == 0:
        key_list = (object_key - 3, object_key - 2, object_key - 1, object_key)

    else:
        print("unexpected situation")
    return key_list


def key_list_func_for_L3_8(object_key):
    if object_key % 8 == 1:
        key_list = (object_key, object_key + 1, object_key + 2, object_key + 3, object_key + 4, object_key + 5, object_key + 6, object_key + 7)
    elif object_key % 8 == 2:
        key_list = (object_key, object_key + 1, object_key + 2, object_key + 3, object_key + 4, object_key + 5, object_key + 6, object_key - 1)
    elif object_key % 8 == 3:
        key_list = (object_key, object_key + 1, object_key + 2, object_key + 3, object_key + 4, object_key + 5, object_key - 2, object_key -1)
    elif object_key % 8 == 4:
        key_list = (object_key, object_key + 1, object_key + 2, object_key + 3, object_key + 4, object_key -3, object_key -2, object_key -1)
    elif object_key % 8 == 5:
        key_list = (object_key, object_key + 1, object_key + 2, object_key + 3, object_key - 4, object_key -3, object_key -2, object_key -1)
    elif object_key % 8 == 6:
        key_list = (object_key, object_key + 1, object_key + 2, object_key -5, object_key - 4, object_key -3, object_key -2, object_key -1)
    elif object_key % 8 == 7:
        key_list = (object_key, object_key + 1, object_key -6, object_key -5, object_key - 4, object_key -3, object_key -2, object_key -1)
    elif object_key % 8 == 0:
        key_list = (object_key, object_key + 1, object_key -7, object_key -5, object_key - 4, object_key -3, object_key -2, object_key -1)
    else:
        print("unexpected situation")
    return key_list

def key_list_func_for_L2(object_key):
    if object_key % 2 == 0:
        key_list = (object_key - 1, object_key)
    elif object_key % 2 == 1:
        key_list = (object_key, object_key + 1)
    else:
        print("unexpected situation")
    return key_list


# key_list_func 에서 구한 키 인덱스 리스트로 key 리스트를 가져옴 가져옴
def return_key(key_list, index_dict):
    values = []
    for key in key_list:
        values.append(index_dict[key])
    return values


# key_list의 key에 대응되는 value를 src_layer에서 찾아서 target_layer에 넣어줌. target이 src보다 높은 차원
def put_into_layer(key_list, target_layer, src_layer):
    for value in key_list:
        target_layer[value] = src_layer[value]
    return target_layer


def move_to_end(layer, key_list):
    ord_layer = collections.OrderedDict(layer)
    for key in key_list:
        ord_layer.move_to_end(key, last=True)
    return ord_layer


def list_by_weight(original_cell, n):
    name_list = original_cell['Symbol'].values.tolist()
    weight_list = original_cell['Volume'].values.tolist()
    list = random.choices(name_list, weights=weight_list, k=n)
    return list


def L3(value, src_layer):
    # L4를 인덱싱한 딕셔너리로 전환
    index_list = dict(enumerate(src_layer, 1))
    target_key = search(value, index_list)
    indexed_key_list = key_list_func_for_L3(target_key)
    object_key_list = return_key(indexed_key_list, index_list)
    result = put_into_layer(object_key_list, L3_layer, src_layer)
    return result, object_key_list


def L2(value, src_layer):
    index_list = dict(enumerate(src_layer, 1))
    target_key = search(value, index_list)
    indexed_key_list = key_list_func_for_L2(target_key)
    object_key_list = return_key(indexed_key_list, index_list)
    result = put_into_layer(object_key_list, L2_layer, src_layer)
    return result, object_key_list


def L1(value, src_layer):
    index_list = dict(enumerate(src_layer, 1))
    target_key = search(value, index_list)
    indexed_key_list = key_list_func_for_L2(target_key)
    object_key_list = return_key(indexed_key_list, index_list)
    result = {value: src_layer[value]}
    return result, object_key_list


L3_layer = {}
L2_layer = {}
L1_layer = {}

hit_L1 = 0
hit_L2 = 0
hit_L3 = 0

count1 = 0
count2 = 0
count3 = 0

miss_L1 = count1 - hit_L1
miss_L2 = count2 - hit_L2
miss_L3 = count3 - hit_L3

L3_layer = {}
L2_layer = {}
L1_layer = {}

key = 0
L4_layer = original_dict
L3_layer = OrderedDict(L3_layer)
L2_layer = OrderedDict(L2_layer)
L1_layer = OrderedDict(L1_layer)

key_weight_list = list_by_weight(original_data, 10000)
#print(key_weight_list)

#for key in key_weight_list:
while key != 'exit':
    key = input("Input symbol : ")
    if key in L1_layer:
        hit_L1 += 1
        count1 += 1
        print(L1_layer[key])

    else:  # L1 miss
        miss_L1 += 1
        count1 += 1
        if decide_in_layer(key, L2_layer):
            hit_L2 += 1
            count2 += 1
            L1_layer, l1_key_list = L1(key, L2_layer)
            L2_layer = move_to_end(L2_layer, l1_key_list)
            print(L1_layer[key])

        else:  # level 2 miss
            miss_L2 += 1
            count2 += 1
            if isFull(L2_layer, 16):
                L2_layer.popitem(last=False)
                L2_layer.popitem(last=False)
                if decide_in_layer(key, L3_layer):
                    hit_L3 += 1
                    count3 += 1
                    L2_layer, l2_key_list = L2(key, L3_layer)
                    L3_layer = move_to_end(L3_layer, l2_key_list)
                    L1_layer.clear()
                    L1_layer = {key: L2_layer[key]}
                    print(L1_layer[key])

                else:  # level3 miss
                    miss_L3 += 1
                    count3 += 1
                    if isFull(L3_layer, 256):
                        #L3_layer.popitem(last=False) iterated by 4 times
                        L3_layer.popitem(last=False)
                        L3_layer.popitem(last=False)
                        L3_layer.popitem(last=False)
                        L3_layer.popitem(last=False)

                        L3_layer, l3_key_list = L3(key, L4_layer)
                        L2_layer, l2_key_list = L2(key, L3_layer)
                        L1_layer.clear()
                        L1_layer = {key: L2_layer[key]}
                        print(L1_layer)
                    else:  # level3 not full
                        L3_layer, l3_key_list = L3(key, L4_layer)
                        L2_layer, l2_key_list = L2(key, L3_layer)
                        L1_layer.clear()
                        L1_layer = {key: L2_layer[key]}
                        print(L1_layer)
            else:  # level2 not full
                if decide_in_layer(key, L3_layer):
                    hit_L3 += 1
                    count3 += 1
                    L2_layer, l2_key_list = L2(key, L3_layer)
                    L3_layer = move_to_end(L3_layer, l2_key_list)
                    L1_layer.clear()
                    L1_layer = {key: L2_layer[key]}
                    print(L1_layer)
                else:  # level3 miss
                    miss_L3 += 1
                    count3 += 1
                    L3_layer, l3_key_list = L3(key, L4_layer)
                    L2_layer, l2_key_list = L2(key, L3_layer)
                    L1_layer.clear()
                    L1_layer = {key: L2_layer[key]}
                    print(L1_layer)
    print("L1 hit ratio : ", hit_L1 / count1)
    print("L2 hit ratio : ", hit_L2 / count2)
    print("L3 hit ratio : ", hit_L3 / count3)

    print("L1 miss ratio : ", miss_L1 / count1)
    print("L2 miss ratio : ", miss_L2 / count2)
    print("L3 miss ratio : ", miss_L3 / count3)

    print(L1_layer.keys())
    print(L2_layer.keys())
    print(L3_layer.keys())
  #      break



