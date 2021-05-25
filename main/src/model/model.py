import csv
import os

from .bm25hf import BM25HF,change_bm25hf,find_words_from_bm25hf_mat
from .bm25hf import words_to_add_bm25hf_string
from .kmeans import KMeans
from .bm25hf import Corpus
class BM25HF_KMeans:
    def __init__(self,args):
        self.saved_filter_person_file = os.path.join(args.processed_path,"NLP_Corpus_Persons_Article.json")
        corpus = Corpus(self.saved_filter_person_file)
        self.bm25hf = BM25HF(corpus)
        bm25hf_mat = self.bm25hf.score_all()
        result_mat, self.index2person = change_bm25hf(bm25hf_mat)
        self.kmeans = KMeans(result_mat, args.num_topics, args.max_iter)
        self.num_words = args.num_words
        self.topic_words = {}
    def run(self):
        self.kmeans.run()
        assignments = self.kmeans.get_assignments()
        # 进行候选词抽取方法
        means_centers = {}
        for assign_index,center_person_id in enumerate(assignments):
            person_id = self.index2person[assign_index]
            if center_person_id not in means_centers:
                means_centers[center_person_id] = []
                means_centers[center_person_id].append(person_id)
            else:
                means_centers[center_person_id].append(person_id)
        num = 0
        in_num = 0
        for key in means_centers:
            num += len(means_centers[key])
            if key in means_centers[key]:
                in_num += 1
        for center_person_id in means_centers:
            person_list = means_centers[center_person_id]
            words_list = find_words_from_bm25hf_mat(self.bm25hf.bm25hf_mat,person_list,self.num_words)
            self.topic_words[center_person_id] = words_to_add_bm25hf_string(words_list)
    def save_topics(self,logger,save_topics_file,save_results_file):
        topics_list = [[topic_id,self.topic_words[topic_id]] for topic_id in self.topic_words]
        with open(save_topics_file,mode="w",encoding="utf-8") as wfp:
            writer = csv.writer(wfp)
            writer.writerows(topics_list)
        logger.info("Saved in file:%s"%save_topics_file)
        assignments = self.kmeans.get_assignments()
        all_assignments = []
        for item in assignments:
            tp_list = [self.index2person[item],item]
            all_assignments.append(tp_list)
        with open(save_results_file,mode="w",encoding="utf-8") as wfp:
            writer = csv.writer(wfp)
            writer.writerows(all_assignments)
        logger.info("Saved in file:%s" % save_results_file)


