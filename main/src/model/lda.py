import os
import json
import csv
from gensim import corpora,models
class LDA:
    def __init__(self,args):
        self.num_topics = args.num_topics
        self.ids = []
        self.dataset = []
        self.lda = None
        self.root_path = args.root_path
        if not os.path.exists(self.root_path):
            os.mkdir(self.root_path)
        self.num_words = args.num_words
        self.alpha = args.alpha
        self.beta = args.beta
        self.topic_result_file = os.path.join(self.root_path,"topics_results.csv")
        self.document_result_file = os.path.join(self.root_path, "document_topics_results.csv")
        self.document_max_result_file = os.path.join(self.root_path, "document_max_topics_results.csv")
        self.saved_filter_file = os.path.join(args.processed_path,"NLP_Corpus_Filter.json")
        self.save_file = os.path.join(self.root_path,"NLP_Corpus_lda.mdl")
        #准备好训练语料，整理成gensim需要的输入格式
        with open(self.saved_filter_file,mode="r",encoding="utf-8") as rfp:
            dataset = json.load(rfp)
        for item in dataset:
            self.ids.append(item[0])
            self.dataset.append(item[1])
    def run(self):
        # 构建词频矩阵，训练LDA模型
        self.dictionary = corpora.Dictionary(self.dataset)
        # corpus是把每条新闻ID化后的结果，每个元素是新闻中的每个词语，在字典中的ID和频率
        corpus = [self.dictionary.doc2bow(text) for text in self.dataset]
        self.lda = models.LdaModel(corpus=corpus, id2word=self.dictionary, num_topics=self.num_topics,
                                   alpha=self.alpha,eta=self.beta)
    def save(self,logger,topic_result_file,document_max_result_file):
        corpus = [self.dictionary.doc2bow(text) for text in self.dataset]
        lda_corpus = self.lda[corpus]
        topic_list = self.lda.print_topics(self.num_topics,self.num_words)
        # 保存主题
        with open(topic_result_file,mode="w",encoding="utf-8") as wfp:
            writer = csv.writer(wfp)
            for item in topic_list:
                writer.writerow(item)
        logger.info("Results save in file%s"%topic_result_file)


        # 保存文档分类结果
        with open(self.document_result_file, mode="w", encoding="utf-8") as wfp:
            writer = csv.writer(wfp)
            for idx, item in zip(self.ids, lda_corpus):
                writer.writerow([idx] + item)
        logger.info("Results save in file%s" % self.document_result_file)

        # 保存最大概率主题
        lda_topics_list = []
        for index, row in zip(self.ids, lda_corpus):
            max_topic_index = row[0][0]
            max_topic_prob = row[0][1]
            for item in row:
                if item[1] > max_topic_prob:
                    max_topic_prob = item[1]
                    max_topic_index = item[0]
            lda_topics_list.append([index, max_topic_index])
        with open(document_max_result_file, mode="w", encoding="utf-8") as wfp:
            writer = csv.writer(wfp)
            for item in lda_topics_list:
                writer.writerow(item)
        logger.info("Results save in file%s" % document_max_result_file)
        # 保存模型
        self.lda.save(self.save_file)
        logger.info("Model save in file%s" % self.document_result_file)
        self.max_prob_list = lda_topics_list
    def get_max_list(self):
        return self.max_prob_list
    def load(self,save_file):
        self.lda = models.LdaModel.load(save_file)

