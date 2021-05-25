import datetime
import json

import numpy as np


def calculate(a1,a2,a3,alpha=1.0,beta=1.0,gamma=1.0,c = 1.0):
    v_a = (a1*a2*(alpha**2+beta**2)+a1*a3*(alpha**2+gamma**2)+a2*a3*(beta**2+gamma**2)+gamma*a1)
    v_b = (a1*alpha**2+a2*beta**2+a3*gamma**2 + c)
    return v_a/v_b
def get_date(x):
    year, month, day = x[0].split('/')
    year, month, day = int(year),int(month),int(day)
    tp_date = datetime.date(year,month,day)
    return tp_date
def get_year(x):
    year, month = x[0].split('/')
    year, month= int(year),int(month)
    tp_date = datetime.date(year,month,1)
    return tp_date
def get_hot_times_rate(save_markov_file):
    with open(save_markov_file,mode="r",encoding='utf-8') as rfp:
        raw_data = json.load(rfp)
        list_val = []
        max_v = 0
        min_v = float('inf')
        for time1 in raw_data:
            tp_list = raw_data[time1]
            value = 0
            for topic_id in tp_list:
                a1 = tp_list[topic_id]['number']
                a2 = tp_list[topic_id]['discuss']
                a3 = tp_list[topic_id]['transmit']
                v = calculate(a1,a2,a3)
                value += v
            if value>max_v:max_v = value
            if value<min_v:min_v = value
            list_val.append([time1,value])
    list_val = [[item[0],(item[1]-min_v)/(max_v-min_v)] for item in list_val]
    list_val = sorted(list_val,key=lambda x:get_date(x))
    np_val_list = [item[1] for item in list_val]
    time_val_list = [item[0] for item in list_val]
    return time_val_list,np_val_list
def get_month_rate(save_markov_file):
    with open(save_markov_file, mode="r", encoding='utf-8') as rfp:
        raw_data = json.load(rfp)
        list_val = {}

        for time1 in raw_data:
            tp_list = raw_data[time1]
            year,month,day = time1.split('/')
            timeA = year + '/' + month
            if timeA not in list_val:
                list_val[timeA] = {}
            for topic_id in tp_list:
                if topic_id not in list_val[timeA]:
                    list_val[timeA][topic_id] = {
                        "number": tp_list[topic_id]['number'],
                        "discuss": tp_list[topic_id]['discuss'],
                        "transmit": tp_list[topic_id]['transmit']
                    }
                else:
                    list_val[timeA][topic_id]['number'] += tp_list[topic_id]['number']
                    list_val[timeA][topic_id]['discuss'] += tp_list[topic_id]['discuss']
                    list_val[timeA][topic_id]['transmit'] += tp_list[topic_id]['transmit']
        final_list = []
        max_v = 0
        min_v = float('inf')
        for time1 in list_val:
            tp_list = list_val[time1]
            value = 0
            for topic_id in tp_list:
                a1 = tp_list[topic_id]['number']
                a2 = tp_list[topic_id]['discuss']
                a3 = tp_list[topic_id]['transmit']
                v = calculate(a1, a2, a3)
                value += v
            if value > max_v: max_v = value
            if value < min_v: min_v = value
            final_list.append([time1, value])
    final_list = [[item[0], (item[1] - min_v) / (max_v - min_v)] for item in final_list]
    final_list = sorted(final_list, key=lambda x: get_year(x))
    np_val_list = [item[1] for item in final_list]
    time_val_list = [item[0] for item in final_list]
    return time_val_list, np_val_list
def get_markov_trans_mat(raw_mat):
    np_mat = np.array(raw_mat)*100
    length = len(np_mat)
    re_mat = np.zeros(shape=(length-1,),dtype=np.float)
    for k in range(length-1):
        tp_v = np_mat[k+1] - np_mat[k]
        re_mat[k] = tp_v
    max_v = re_mat.max()
    min_v = re_mat.min()

    label_lists = []
    for val in re_mat:
        if val >= min_v and val < 2*min_v/3:
            label_lists.append('S6')
        elif val >= 2*min_v/3 and val < min_v/3:
            label_lists.append('S5')
        elif val >= min_v/3 and val < 0:
            label_lists.append('S4')
        elif val >= 0 and val < max_v/3:
            label_lists.append('S3')
        elif val >= max_v/3 and val < 2*max_v/3:
            label_lists.append('S2')
        elif val >= 2*max_v/3 and val <= max_v:
            label_lists.append('S1')
    trans_mat = np.zeros(shape=(6,6),dtype=np.float)
    for tp1 in label_lists:
        tp_id1 = int(tp1.replace('S',''))-1
        for tp2 in label_lists:
            tp_id2 = int(tp2.replace('S', ''))-1
            trans_mat[tp_id1,tp_id2] += 1
    trans_mat = trans_mat/trans_mat.sum()
    pi_vec = np.zeros(shape=(1,6),dtype=np.float)
    tp_id = int(label_lists[0].replace('S',''))-1
    pi_vec[0][tp_id] = 1
    rights_nums = 0
    for k,label in enumerate(label_lists[1:]):
        pi_vec = pi_vec.dot(trans_mat**k)
        if int(np.argmax(pi_vec)) == int(label_lists[k].replace('S',''))-1:
            rights_nums += 1
    return rights_nums,len(label_lists)





