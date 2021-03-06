import os
import csv
import random
import json
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib.dates as mdate

from ...data import TimeDataLoader


def random_color():
    colors1 = '0123456789ABCDEF'
    num = "#"
    for i in range(6):
        num += random.choice(colors1)
    return num


def get_color_list(num_topics):
    color_list = []
    while len(color_list) != num_topics:
        color = random_color()
        if color not in color_list:
            color_list.append(color)
    return color_list

def get_time_to_topics(article_to_topics,save_json):
    allDict = {}
    with open(save_json, mode="r", encoding='utf-8') as rfp:
        raw_data = json.load(rfp)
        for item in raw_data:
            time1 = item['time'].split()[0]
            idx = item['id']
            if time1 not in allDict:
                allDict[time1] = {}
                if idx in article_to_topics:
                    topic_index = article_to_topics[idx]
                    if topic_index not in allDict[time1]:
                        allDict[time1][topic_index] = 1
                    else:
                        allDict[time1][topic_index] += 1
            else:
                if idx in article_to_topics:
                    topic_index = article_to_topics[idx]
                    if topic_index not in allDict[time1]:
                        allDict[time1][topic_index] = 1
                    else:
                        allDict[time1][topic_index] += 1
    return allDict
def make_topics_times(root_path,saved_file,all_dict,name,batch_size):
    num_topics = 0
    with open(saved_file,mode="r",encoding="utf-8") as rfp:
        reader = csv.reader(rfp)
        for _ in reader:
            num_topics += 1
    tmp_dict = {}
    for item in tqdm(all_dict):
        if len(all_dict[item]) == 0:
            continue
        index = list(all_dict[item].keys())[0]
        max_value = list(all_dict[item].values())[0]
        for key in all_dict[item]:
            if max_value < all_dict[item][key]:
                index = key
                max_value = all_dict[item][key]
        tmp_dict[item] = [index, max_value]
    dataloader = TimeDataLoader(tmp_dict, batch_size)

    for num in range(len(dataloader)):
        save_fig = os.path.join(root_path, 'pic_time_topics_%s%d.png' % (name, num))
        draw_topic_max(save_fig,dataloader[num],num_topics)
def draw_topic_max(save_fig,dataset,num_topics):
    time_list,raw_data = dataset
    data_list = [item[1] for item in raw_data]
    topic_index = [item[0] for item in raw_data]
    # ????????????????????????
    color_list = get_color_list(num_topics)

    # ?????????????????????
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    # ??????????????????
    fig = plt.figure(figsize=(70, 9))
    # ?????????????????????????????????
    ax = plt.subplot(111)
    # ???????????????  ?????? ??? x???????????? ???????????????
    ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d'))
    # ???X???????????????
    plt.xticks(time_list, rotation=45)
    # ?????????
    ax.plot(time_list, data_list, color='r')
    # ??????
    for x,y,ids in zip(time_list,data_list,topic_index):
        ax.scatter(x,y,c=color_list[int(ids)],label = '??????%s'%ids)
    # ????????????
    ax.set_title('?????????????????????')
    # ?????? x y ?????????
    ax.set_xlabel('??????', fontsize=20)
    ax.set_ylabel('????????????', fontsize=20)
    plt.legend(loc='upper right')
    plt.savefig(save_fig)
    plt.close()
