import datetime
import json
import os
import torch.utils.data as data
from .vetorize import vectorize
import numpy as np
import matplotlib.pyplot as plt

def get_date(item):
    year,month,day = item[0].split("/")
    year, month, day = int(year),int(month),int(day)
    value = datetime.date(year,month,day)
    return value
class Dictionary(object):
    PAD = '<PAD>'
    UNK = '<UNK>'
    START = 2
    def __init__(self):
        self.tok2ind = {self.PAD: 0, self.UNK: 1}
        self.ind2tok = {0: self.PAD, 1: self.UNK}

    def __len__(self):
        return len(self.tok2ind)

    def __iter__(self):
        return iter(self.tok2ind)

    def __contains__(self, key):
        if type(key) == int:
            return key in self.ind2tok
        elif type(key) == str:
            return key in self.tok2ind

    def __getitem__(self, key):
        if type(key) == int:
            return self.ind2tok.get(key, self.UNK)
        if type(key) == str:
            return self.tok2ind.get(key,self.tok2ind.get(self.UNK))

    def __setitem__(self, key, item):
        if type(key) == int and type(item) == str:
            self.ind2tok[key] = item
        elif type(key) == str and type(item) == int:
            self.tok2ind[key] = item
        else:
            raise RuntimeError('Invalid (key, item) types.')
    def add(self, token):
        if token not in self.tok2ind:
            index = len(self.tok2ind)
            self.tok2ind[token] = index
            self.ind2tok[index] = token
    def tokens(self):
        """Get dictionary tokens.
        Return all the words indexed by this dictionary, except for special
        tokens.
        """
        tokens = [k for k in self.tok2ind.keys()
                  if k not in {'<NULL>', '<UNK>'}]
        return tokens
    def save(self,save_dict_file):
        with open(save_dict_file,mode="w",encoding="utf-8") as wfp:
            tp_dict = {
                "ind2tok":self.ind2tok,
                "tok2ind":self.tok2ind
            }
            json.dump(tp_dict,wfp)
    @staticmethod
    def load(save_dict_file):
        with open(save_dict_file,mode="r",encoding="utf-8") as rfp:
            tp_dict = json.load(rfp)
            dictionary = Dictionary()
            dictionary.tok2ind = tp_dict['tok2ind']
            dictionary.ind2tok = tp_dict['ind2tok']
            return dictionary
def build_dict(word_dict,save_file):
    with open(save_file, mode="r", encoding="utf-8") as rfp:
        dataset = json.load(rfp)
    for item in dataset:
        inputs = item['input']
        targets = item['target']
        for doc in inputs:
            for word in doc[1]:
                word_dict.add(word)
        word_dict.add(targets[1])
class NLPDataset(data.Dataset):
    def __init__(self,save_dataset_times_json,dictionary):
        with open(save_dataset_times_json, mode="r", encoding="utf-8") as rfp:
            self.dataset = json.load(rfp)
        # build word vocabulary
        self.word_dict = dictionary
        self.length = len(self.dataset)
        self.num_days = len(self.dataset[0])
    def __getitem__(self, item):
        return vectorize(self.dataset[item],self.word_dict)
    def __len__(self):
        return self.length
def draw_data(data_list, title, save_fig):
    x = np.linspace(0, len(data_list) - 1, len(data_list))
    # 中文乱码的处理
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.plot(x, data_list)
    plt.title(title)
    plt.xlabel("训练次数")
    plt.ylabel("数量值")
    plt.savefig(save_fig)
    plt.show()
    plt.close()
class TimeSaver:
    def __init__(self,log_path):
        self.log_path = log_path
        self.test_acc = []
        self.test_acc_a = []
        self.test_acc_b = []
        self.test_loss = []
    def add(self,test_acc,test_acc_a,test_acc_b,test_loss):
        self.test_acc.append(test_acc)
        self.test_acc_a.append(test_acc_a)
        self.test_acc_b.append(test_acc_b)
        self.test_loss.append(test_loss)
    def draw(self):
        save_fig = os.path.join(self.log_path, 'loss.png')
        draw_data(self.test_loss, "损失函数值变化图", save_fig)
        save_fig = os.path.join(self.log_path, 'acc.png')
        draw_data(self.test_acc, "总精确值变化图", save_fig)
        save_fig = os.path.join(self.log_path, 'acc_a.png')
        draw_data(self.test_acc_a, "预测天数精确值变化图", save_fig)
        save_fig = os.path.join(self.log_path, 'acc_b.png')
        draw_data(self.test_acc_b, "预测热词精确值变化图", save_fig)
    def save_best(self):
        best_acc = max(self.test_acc)
        best_acc_a = max(self.test_acc_a)
        best_acc_b = max(self.test_acc_b)
        save_best_file = os.path.join(self.log_path, 'best.txt')
        with open(save_best_file,mode="w",encoding="utf-8") as wfp:
            wfp.write("best acc:%0.5f\n"%best_acc)
            wfp.write("best acc:%0.5f\n"%best_acc_a)
            wfp.write("best acc:%0.5f\n"%best_acc_b)

