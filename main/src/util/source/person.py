import csv

from tqdm import tqdm
import json
import matplotlib.pyplot as plt

from ...data import Vocabulary
from .draw import draw_frequency
def draw_person_frequency(person_freq_file,save_freq_person,length):
    dictWords = []
    with open(person_freq_file, mode="r", encoding="utf-8") as rfp:
        reader = csv.reader(rfp)
        for item in reader:
            word = item[0]
            freq = item[1]
            dictWords.append([word, int(freq)])

    title = 'Top%d用户数量分布' % length
    x_label = '用户数目排序'
    y_label = '数量'
    draw_frequency(dictWords,save_freq_person,length,title,x_label,y_label)
def get_person_frequency(save_json,save_file,sorted_list = True,cal_same= False):
    with open(save_json, mode="r", encoding="utf-8") as rfp:
        raw_data = json.load(rfp)
        num_data = {}
        for item in tqdm(raw_data, desc='person count'):
            person_id = item['person_id']
            article = item['article']
            if article.strip() =='':
                continue
            if not cal_same:
                if person_id not in num_data:
                    num_data[person_id] = set()
                    num_data[person_id].add(article)
                else:
                    num_data[person_id].add(article)
            else:
                if person_id not in num_data:
                    num_data[person_id] = 1
                else:
                    num_data[person_id] += 1
    save_data = []
    for item in num_data:
        if not cal_same:
            save_data.append([item ,len(num_data[item])])
        else:
            save_data.append([item ,num_data[item]])
    if sorted_list:
        save_data = sorted(save_data,key=lambda x:x[1])
    with open(save_file,mode="w",encoding="utf-8") as wfp:
        writer = csv.writer(wfp)
        writer.writerows(save_data)
def draw_person_frequency_peoples(person_freq_file,save_freq_person_peoples):
    dictWords = {}
    with open(person_freq_file, mode="r", encoding="utf-8") as rfp:
        reader = csv.reader(rfp)
        for item in reader:
            word = item[0]
            freq = item[1]
            dictWords[word]=int(freq)
    one_comments_people = 0
    two_comments_people = 0
    ten_comments_people = 0
    hundred_comments_people = 0
    thousand_comments_people = 0
    up_comments_people = 0
    for word in dictWords:
        if dictWords[word] == 1:
            one_comments_people += 1
        if dictWords[word] == 2:
            two_comments_people += 1
        if dictWords[word] >= 3 and dictWords[word] <= 10:
            ten_comments_people += 1
        if dictWords[word] >= 10 and dictWords[word] <= 100:
            hundred_comments_people += 1
        if dictWords[word] >= 100 and dictWords[word] <= 1000:
            thousand_comments_people += 1
        if dictWords[word] >= 1000:
            up_comments_people += 1
    # 画出对应的条形统计图
    y_title = ["1","2","3-10","10-100","100-1000","1000以上"]
    freq_list = [one_comments_people,two_comments_people,ten_comments_people,hundred_comments_people,thousand_comments_people,up_comments_people]
    length = len(freq_list)
    x_list = range(length)
    # 中文乱码的处理
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False

    plt.figure(figsize=(10,6))
    plt.bar(x_list, freq_list, align='center', alpha=0.8, width=0.8)
    plt.xticks(x_list, y_title)
    plt.xlabel('发表评论的数量')
    plt.ylabel('用户数量')
    plt.title('发表评论数据分布')
    # 给条形图添加数据标注
    for x,y in enumerate(freq_list):
        plt.text(x, y+1, "%s" % y)
    plt.savefig(save_freq_person_peoples)
    plt.close()
