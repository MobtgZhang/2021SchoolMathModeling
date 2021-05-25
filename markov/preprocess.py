import json
import re
import os
from tqdm import tqdm
from bs4 import BeautifulSoup
def combine(raw_path,save_file):
    '''
    合并数据文件,将22个数据文件全部合并起来
    注意原始文件是GBK编码的,现在将其转化为UTF-8编码进行操作
    :param file_path: 读取的数据文件
    :param save_file: 保存的数据文件
    :return: 无
    '''
    filenames = os.listdir(raw_path)
    filenames = sorted(filenames,key=lambda x:int(re.findall('NLP_Corpus_(.*).txt',x)[0]))
    with open(save_file,mode="w",encoding="utf-8") as wfp:
        for file in filenames:
            tmp_file = os.path.join(raw_path,file)
            with open(tmp_file, mode="r", encoding="gbk") as rfp:
                for line in rfp:
                    wfp.write(line.strip()+"\n")
def get_person_filter(raw_file,save_person_filter):
    # 筛选出不重复的文章
    all_data = {}
    with open(raw_file,mode="r",encoding="utf-8") as rfp:
        soup = BeautifulSoup(rfp,'lxml')
        for item in tqdm(soup.find_all("record"),desc="bs4 filter processing"):
            idx = item.id.get_text().strip()
            article = item.article.get_text().strip()
            if article.strip() == '':
                continue
            discuss = item.discuss.get_text().strip()
            person_id = item.person_id.get_text().strip()
            time1 = item.time.get_text().strip()
            transmit = item.transmit.get_text().strip()
            if person_id not in all_data:
                all_data[person_id] = {}
                all_data[person_id][article] = {
                    "id": idx,
                    "time": time1,
                    "transmit": transmit,
                    "discuss": discuss
                }
            else:
                if article in all_data[person_id]:
                    continue
                else:
                    all_data[person_id][article] = {
                        "id": idx,
                        "time":time1,
                        "transmit":transmit,
                        "discuss":discuss
                    }
    re_filter_data = {}
    for person_id in tqdm(all_data,'exchange,filter and segment data'):
        for article in all_data[person_id]:
            idx = all_data[person_id][article]['id']
            time1 = all_data[person_id][article]['time']
            transmit = all_data[person_id][article]['transmit']
            discuss = all_data[person_id][article]['discuss']
            if article.strip() == '':
                continue
            if time1 not in re_filter_data:
                re_filter_data[time1] = {}
                if len(time1.split()) == 2:
                    pass
                else:
                    raise Exception(str(time1))
                re_filter_data[time1][idx] = {
                    "article": article,
                    "transmit": transmit,
                    "discuss": discuss,
                    "person_id":person_id
                }
            else:
                re_filter_data[time1][idx] = {
                    "article": article,
                    "transmit": transmit,
                    "discuss": discuss,
                    "person_id": person_id
                }
    del all_data
    with open(save_person_filter,mode="w",encoding="utf-8") as wfp:
        json.dump(re_filter_data,wfp)
def get_days_items(save_json,topic_words_file,save_markov_file):
    topic_dict = []
    with open(topic_words_file, mode="r", encoding="utf-8") as rfp:
        for line in rfp:
            items = set(line.strip().split('、'))
            topic_dict.append(items)
    all_data = {}
    with open(save_json, mode="r", encoding="utf-8") as rfp:
        raw_data = json.load(rfp)
        for time1 in tqdm(raw_data,desc='iter '):
            item1,item2 = time1.split()
            if item1 not in all_data:
                all_data[item1] = raw_data[time1]
            else:
                all_data[item1].update(raw_data[time1])
    topics_data = {}
    for time1 in tqdm(all_data,desc='build '):
        topics_data[time1] = {}
        for idx in all_data[time1]:
            item = all_data[time1][idx]
            article = item['article']
            discuss = item['discuss']
            transmit = item['transmit']
            for idx,tp_list in enumerate(topic_dict):
                topics_data[time1][idx] = {
                    'number':0,
                    'discuss':0,
                    'transmit':0
                }
                for word in tp_list:
                    if word in article:
                        topics_data[time1][idx]['number'] += 1
                        topics_data[time1][idx]['discuss'] += int(discuss) if discuss.strip()!='' else 0
                        topics_data[time1][idx]['transmit'] += int(transmit) if discuss.strip()!='' else 0
    with open(save_markov_file, mode="w", encoding="utf-8") as wfp:
        json.dump(topics_data,wfp)
















