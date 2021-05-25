import csv
import json
import matplotlib.pyplot as plt
from .draw import draw_frequency
def get_trans_dis_frequency(save_json, freq_file,typeid):
    typeid = typeid.lower()
    assert typeid in ['transmit','discuss']
    with open(save_json,mode="r",encoding="utf-8") as rfp:
        all_raw = json.load(rfp)
    all_data = []
    for item in all_raw:
        if typeid.lower() == 'transmit':
            if item['transmit'].strip() == "":
                all_data.append([item['person_id'], item['id'],-1])
            else:
                all_data.append([item['person_id'], item['id'],int(item['transmit'])])
        if typeid.lower() == 'discuss':
            if item['discuss'].strip() == "":
                all_data.append([item['person_id'], item['id'], -1])
            else:
                all_data.append([item['person_id'], item['id'], int(item['discuss'])])
    all_data = sorted(all_data,key=lambda x:x[2],reverse=True)
    with open(freq_file,mode="w",encoding="utf-8") as wfp:
        for item in all_data:
            line = ""
            for word in item:
                line = line + str(word)+","
            wfp.write(line+"\n")
def draw_trans_dis_frequency(transmit_freq_file,save_freq_transmit_fig,top_num,name):
    dictWords = []
    with open(transmit_freq_file, mode="r", encoding="utf-8") as rfp:
        reader = csv.reader(rfp)
        for item in reader:
            dictWords.append(["用户:%s\n文章:%s\n"%(item[0],item[1]),int(item[1])])
    title = 'Top%d %s数量分布' % (top_num,name)
    x_label = '数目排序'
    y_label = '数量'
    draw_frequency(dictWords, save_freq_transmit_fig, top_num, title, x_label, y_label)
def draw_trasmit_frequency_distribution(freq_file,save_freq_trans_dis,typeid):
    dictWords = {}
    with open(freq_file, mode="r", encoding="utf-8") as rfp:
        reader = csv.reader(rfp)
        for item in reader:
            word = '%s_%s'%(item[0],item[1])
            dictWords[word] = int(item[2])
    none_comments_people = 0
    zero_comments_people = 0
    ten_comments_people = 0
    hundred_comments_people = 0
    thousand_comments_people = 0
    up1_comments_people = 0
    up2_comments_people = 0
    for word in dictWords:
        if dictWords[word] == -1:
            none_comments_people += 1
        if dictWords[word] == 0:
            zero_comments_people += 1
        if dictWords[word] <= 10:
            ten_comments_people += 1
        if dictWords[word] >= 10 and dictWords[word] <= 100:
            hundred_comments_people += 1
        if dictWords[word] >= 100 and dictWords[word] <= 1000:
            thousand_comments_people += 1
        if dictWords[word] >= 1000 and dictWords[word] <= 10000:
            up1_comments_people += 1
        if dictWords[word] >= 10000:
            up2_comments_people += 1
    # 画出对应的条形统计图
    y_title = ["未指定","0","1-10", "10-100", "100-1000", "1000-10000","10000以上"]
    freq_list = [none_comments_people,zero_comments_people,ten_comments_people, hundred_comments_people,
                 thousand_comments_people, up1_comments_people, up2_comments_people]
    length = len(freq_list)
    x_list = range(length)
    # 中文乱码的处理
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False

    plt.figure(figsize=(10, 6))
    plt.bar(x_list, freq_list, align='center', alpha=0.8, width=0.8)
    plt.xticks(x_list, y_title)
    plt.xlabel('发表评论的数量')
    plt.ylabel('数量')
    plt.title('%s数据分布'%typeid)
    # 给条形图添加数据标注
    for x, y in enumerate(freq_list):
        plt.text(x, y + 1, "%s" % y)
    plt.savefig(save_freq_trans_dis)
    plt.close()

def draw_trasmit_frequency_distribution_lessNum(save_json,transmit_freq_file,number,save_freq_transmit_dis_fig, name):
    dictWords = {}
    with open(save_json,mode="r",encoding="utf-8") as rfp:
        raw_data = json.load(rfp)
        for item in raw_data:
            if item['person_id'] not in dictWords:
                dictWords[item['person_id']] = {}
                dictWords[item['person_id']]['length'] = 1
                dictWords[item['person_id']][name] = item[name]
            else:
                dictWords[item['person_id']]['length'] += 1
                dictWords[item['person_id']][name] += item[name]
    for item in dictWords:
        value = dictWords[item][name]/dictWords[item]['length']
        dictWords[item] = [value]
    dictWords = sorted(dictWords,key=lambda x:x[1],reverse=True)
