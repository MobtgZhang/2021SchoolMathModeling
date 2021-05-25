import json
import math
from tqdm import tqdm
from .preprocess import jieba_segment,filter_chinese
def get_person_filter(save_json,save_person_filter,stop_words_file,jieba = True,singleWords=False):
    all_data = {}
    # 筛选出不重复的文章
    with open(save_json,mode="r",encoding="utf-8") as rfp:
        raw_data = json.load(rfp)
        for item in tqdm(raw_data,'creating person data'):
            person_id = item['person_id']
            article = item['article']
            if article.strip() == '':
                continue
            time1 = item['time']
            time2 = item['insertTime']
            transmit = item['transmit']
            discuss = item['discuss']
            idx = item['id']
            if person_id in all_data:
                if article in all_data[person_id]:
                    continue
                else:
                    all_data[person_id][article] = {
                        "id": idx,
                        "time":time1,
                        "transmit":transmit,
                        "discuss":discuss
                    }
            else:
                all_data[person_id] = {}
                all_data[person_id][article] = {
                    "id":idx,
                    "time": time1,
                    "transmit": transmit,
                    "discuss": discuss
                }
    re_filter_data = {}
    for person_id in tqdm(all_data,'exchange,filter and segment data'):
        re_filter_data[person_id] = {}
        for article in all_data[person_id]:
            idx = all_data[person_id][article]['id']
            time1 = all_data[person_id][article]['time']
            transmit = all_data[person_id][article]['transmit']
            discuss = all_data[person_id][article]['discuss']
            if article.strip() == '':
                continue
            document = filter_chinese(article)
            if document != '':
                if jieba:
                    document = jieba_segment(document, stop_words_file, singleWords)
                    if len(document) == 0:
                        continue
                    re_filter_data[person_id][idx] = {
                        "article": document,
                        "time": time1,
                        "transmit": transmit,
                        "discuss": discuss
                    }
    del all_data
    with open(save_person_filter,mode="w",encoding="utf-8") as wfp:
        json.dump(re_filter_data,wfp)
def make_rdf_dict(save_filter_json,save_rdf_file):
    with open(save_filter_json,mode="r",encoding="utf-8") as rfp:
        raw_data = json.load(rfp)
    documents = []
    for person_id in raw_data:
        for article_id in raw_data[person_id]:
            documents.append(raw_data[person_id][article_id]['article'])
    all_num = len(documents)
    f_doc = []
    word2idf = {}
    for doc_index in tqdm(range(all_num), desc='rdf process'):
        tmp = {}
        for word in documents[doc_index]:
            if not word in tmp:
                tmp[word] = 0
            tmp[word] += 1
        f_doc.append(tmp)
        for k, v in tmp.items():
            if k not in f_doc:
                word2idf[k] = 0
            word2idf[k] += 1
    for k, v in word2idf.items():
        word2idf[k] = math.log(all_num - v + 0.5) - math.log(v + 0.5)
    with open(save_rdf_file, mode="w", encoding="utf-8") as wfp:
        json.dump(word2idf, wfp)


















