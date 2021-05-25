import datetime
import json
import os
import random

from tqdm import tqdm

from ..model import BM25HF,Corpus
def get_date(x):
    year,month,day = x[0].split('/')
    year, month, day = int(year),int(month),int(day)
    return datetime.date(year,month,day)
def build_time_series(save_bm25hf_json,save_dataset_json,num_words):
    with open(save_bm25hf_json, mode="r", encoding='utf-8') as rfp:
        raw_data = json.load(rfp)
    dataset_tmp = {}
    for time_day in tqdm(raw_data,desc="process time"):
        tmp_dicts = {}
        for article_id in raw_data[time_day]:
            article = raw_data[time_day][article_id]
            for item in article:
                word = item[0]
                bm25hf = item[1]
                if word not in tmp_dicts:
                    tmp_dicts[word] = bm25hf
                else:
                    tmp_dicts[word] = min(tmp_dicts[word],bm25hf)
        tmp_dicts = list(tmp_dicts.items())
        tmp_dicts = sorted(tmp_dicts,key=lambda x:x[1],reverse=False)
        dataset_tmp[time_day] = tmp_dicts[:num_words]
    with open(save_dataset_json,mode="w",encoding="utf-8") as wfp:
        json.dump(dataset_tmp,wfp)
def build_dataset(save_dataset_times_json,save_dataset_path,time_span,num_days,train_percentage = 0.75):
    if num_days<=2: raise ValueError("num_days must greater than 2!")
    with open(save_dataset_times_json,mode="r",encoding="utf-8") as rfp:
        time_dataset = json.load(rfp)
    # 数据集构建
    datasets_list = []
    for time_day in tqdm(time_dataset,desc="dataset build (time_span %d,num_days %d) "%(time_span,num_days)):
        year, month, day = time_day.split('/')
        year, month, day = int(year), int(month), int(day)
        date_begin = datetime.date(year,month,day)
        delta = datetime.timedelta(days=time_span)
        date_end = date_begin + delta
        tp_list = []
        for time_day_tp in time_dataset:
            year,month,day = time_day_tp.split('/')
            year,month,day = int(year),int(month),int(day)
            date_tp = datetime.date(year,month,day)
            if date_tp >= date_begin and date_tp<=date_end:
                tp_list.append([time_day_tp,time_dataset[time_day_tp]])
            if len(tp_list) == num_days:
                break
        if len(tp_list) < num_days:
            continue
        else:
            # reset parameters
            # 排序
            tp_list = sorted(tp_list,key=lambda x:get_date(x))
            inputs = []
            for item in tp_list[:-1]:
                time1 = item[0]
                word_list = [words[0] for words in item[1]]
                inputs.append([time1,word_list])
            time_target = tp_list[-1][0]
            tmp_list = tp_list[-1][1]
            topwords = sorted(tmp_list,key=lambda x:x[1])
            topwords = topwords[0][0]
            targets = [time_target,topwords]
            datasets_list.append({'input':inputs,'target':targets})
    test_json = os.path.join(save_dataset_path,'test.json')
    train_json = os.path.join(save_dataset_path,'train.json')
    length = len(datasets_list)
    train_len = int(length*train_percentage)
    random.shuffle(datasets_list)
    with open(train_json,mode='w',encoding='utf-8') as wfp:
        json.dump(datasets_list[:train_len],wfp)
    with open(test_json,mode='w',encoding='utf-8') as wfp:
        json.dump(datasets_list[train_len:],wfp)
def build_bm25hf(saved_filter_person_file,save_bm25hf_json):
    corpus = Corpus(saved_filter_person_file)
    bm25hf = BM25HF(corpus)
    bm25hf_mat = bm25hf.score_all()
    dataset = corpus.dataset
    all_time_data = {}
    nums_article = 0
    for person_id in dataset:
        for article_id in dataset[person_id]:
            time1 = dataset[person_id][article_id]['time']
            time_tp,time_tp_day = time1.split()
            article = bm25hf_mat[person_id][article_id]
            nums_article += 1
            if time_tp not in all_time_data:
                all_time_data[time_tp] = {}
                all_time_data[time_tp][article_id] = article
            else:
                all_time_data[time_tp][article_id] = article
    with open(save_bm25hf_json,mode="w",encoding='utf-8') as wfp:
        json.dump(all_time_data,wfp)
