import json
import math
import numpy as np

from tqdm import tqdm
import pickle
class Corpus:
    def __init__(self,save_person_filter):
        self.save_person_filter = save_person_filter
        self.dataset = self.load(save_person_filter)
        self.length = len(self.dataset)
    def load(self,save_person_filter):
        with open(save_person_filter, mode="r", encoding="utf-8") as rfp:
            raw_data = json.load(rfp)
        # 计算总的文章数量
        #value_transmit_all = 0
        #value_discuss_all = 0
        all_history_data = {}
        doc_num_posts = 0
        for person_id in tqdm(raw_data, desc='get A1,A2,A3 and other values'):
            # 1.计算每个用户的博文数量
            tp_len = len(raw_data[person_id])
            if tp_len==0:
                continue
            # 计算文章总量
            doc_num_posts += tp_len
            # 文档编号序列
            all_history_data[person_id] = {}
            value_transmit_user = 0
            value_discuss_user = 0
            for artile_id in raw_data[person_id]:
                doc_user_len = len(raw_data[person_id][artile_id]['article'])
                if doc_user_len == 0:
                    continue
                # 计算每个用户转发博文数量
                text_transmit = raw_data[person_id][artile_id]['transmit']
                value_transmit = 0 if text_transmit.strip() == '' else int(text_transmit)
                value_transmit_user += value_transmit
                # 计算每个用户讨论的数量
                text_discuss = raw_data[person_id][artile_id]['discuss']
                value_discuss = 0 if text_discuss.strip() == '' else int(text_discuss)
                value_discuss_user += value_discuss
                # 计算文章的平均长度

                # 文档
                # 创建词典
                document = raw_data[person_id][artile_id]['article']
                all_history_data[person_id][artile_id] = {
                    'document':document,
                    'value_transmit':value_transmit,
                    'value_discuss':value_discuss,
                    'value_user_num':tp_len
                }
            for artile_id in all_history_data[person_id]:
                if value_transmit_user == 0:
                    vt = 0
                else:
                    vt = all_history_data[person_id][artile_id]['value_transmit'] /value_transmit_user
                if value_discuss_user == 0:
                    vd = 0
                else:
                    vd = all_history_data[person_id][artile_id]['value_discuss'] / value_discuss_user
                all_history_data[person_id][artile_id]['value_transmit'] = vt
                all_history_data[person_id][artile_id]['value_discuss'] = vd
        for person_id in all_history_data:
            for artile_id in all_history_data[person_id]:
                vl = all_history_data[person_id][artile_id]['value_user_num'] / doc_num_posts
                all_history_data[person_id][artile_id]['value_user_num'] = vl
        return all_history_data
    def __getitem__(self, item):
        return self.dataset[item]
    def __len__(self):
        return self.length
    def __str__(self):
        return str(self.dataset)
    def __repr__(self):
        return str(self.dataset)
class BM25HF:
    def __init__(self, docs):
        self.D = len(docs)
        self.avgdl = 0
        num_articles = 0
        self.docs = docs.dataset
        for person_id in self.docs:
            for article_id in docs[person_id]:
                num_articles += 1
                doc = docs[person_id][article_id]['document']
                self.avgdl += len(doc)
        self.avgdl /= num_articles
        self.f = {} # 每一个元素是一个dict，[person_id][article_id] 存储着词频数量
        self.df = {}  # 存储每个词及出现了该词的文档数量
        self.idf = {}  # 存储每个词的idf值
        self.k1 = 1.5
        self.k2 = 0.8
        self.b = 0.75
        self.alpha = 0.8 # 用户文档数量
        self.beta = 1.0 #
        self.gamma = 0.9
        self.init()

    def init(self):
        '''
        :return:
        '''
        for person_id in tqdm(self.docs,desc='initialize'):
            self.f[person_id] = {}
            article_list = self.docs[person_id]

            for artile_id in article_list:
                doc = article_list[artile_id]['document']
                value_discuss = article_list[artile_id]['value_discuss']
                value_transmit = article_list[artile_id]['value_transmit']
                article_nums = article_list[artile_id]['value_user_num']

                v_a = self.alpha**2*article_nums+self.beta**2*value_discuss+value_transmit*self.gamma**2
                v_b = (self.alpha ** 2 + self.beta ** 2) * article_nums * value_discuss + \
                      (self.alpha ** 2 + self.gamma ** 2) * article_nums * value_transmit + \
                      (self.beta ** 2 + self.gamma ** 2) * value_transmit * value_discuss
                value = v_b/v_a
                self.docs[person_id][artile_id]['rhf'] = value
                tmp = {}
                for word in doc:
                    tmp[word] = tmp.get(word, 0) + 1  # 存储每个文档中每个词的出现次数
                self.f[person_id][artile_id] = tmp
                for k in tmp.keys():
                    self.df[k] = self.df.setdefault(k, 0) + 1
        for k, v in self.df.items():
            self.idf[k] = math.log(2*self.D - v + 0.5) - math.log(v + 0.5)
    def score_single(self,doc,person_id,article_id,rhf):
        tp_list = []
        for word in doc:
            d = len(doc)
            tf = self.f[person_id][article_id][word]
            rdf = self.idf[word] * tf
            rtf = (self.k1 + 1)/ (tf+ self.k1 * (1 - self.b + self.b * d/ self.avgdl))
            tp_rhf = (rhf + 1)/(self.k2 + rhf)
            score = rdf*rtf*tp_rhf
            tp_list.append([word,score])
        return tp_list
    def score_all(self):
        bm25hf_mat = {}
        for person_id in tqdm(self.docs,desc='score'):
            articles = self.docs[person_id]
            bm25hf_mat[person_id] = {}
            for article_id in articles:
                rhf = articles[article_id]['rhf']
                document = articles[article_id]['document']
                score_list = self.score_single(document, person_id,article_id,rhf)
                bm25hf_mat[person_id][article_id] = score_list
        self.bm25hf_mat = bm25hf_mat
        return bm25hf_mat
    def save_file(self,save_file):
        with open(save_file, mode="w", encoding="utf-8") as wfp:
            pickle.dump(self,wfp)
def change_bm25hf(bm25hf_mat):
    max_length = 500
    index2person = list(bm25hf_mat.keys())

    dimensions = len(bm25hf_mat)
    result_mat = np.zeros(shape=(dimensions,max_length))
    for k,person_id in enumerate(bm25hf_mat):
        tp_doc_list = []
        for j,article_id in enumerate(bm25hf_mat[person_id]):
            tp_doc_list += bm25hf_mat[person_id][article_id]
        tp_doc_list = sorted(tp_doc_list,key=lambda x:x[1],reverse=True)
        tp_doc_list = tp_doc_list[:max_length]
        for j in range(len(tp_doc_list)):
            result_mat[k,j] = tp_doc_list[j][1]
    return result_mat,index2person
def find_words_from_bm25hf_mat(bm25hf_mat,person_list,num_words):
    words_list = {}
    for person_id in person_list:
        for article_id in bm25hf_mat[person_id]:
            article = bm25hf_mat[person_id][article_id]
            for item in article:
                if item[0] not in words_list:
                    words_list[item[0]] = item[1]
    words_list = [[item,words_list[item]] for item in words_list]
    words_list = sorted(words_list,key=lambda x:x[1],reverse=False)
    return words_list[:num_words]
def words_to_add_bm25hf_string(words_list):
    word_str = ""
    for index,item in enumerate(words_list):
        if index == 0:
            tp_line =  str(item[1])+"*"+ str(item[0])
        else:
            tp_line = "+" + str(item[1]) + "*" + str(item[0])
        word_str += tp_line
    return word_str
