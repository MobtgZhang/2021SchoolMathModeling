import json
import os
import argparse


from log import Logger
from preprocess import combine,get_person_filter,get_days_items
from data import get_hot_times_rate,get_markov_trans_mat,get_month_rate

from draw import draw_hot_rate

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-path",type=str,default="./Data",help="preprocess raw data path.")
    parser.add_argument("--processed-path", type=str, default="./processed", help="processed path.")
    parser.add_argument("--log-path", type=str, default="./log", help="Topic model.")
    parser.add_argument("--topic-words-file", type=str, default="./topic_words.txt", help="topic words file.")
    parser.add_argument("--do-pre", action='store_true', help="Preprocess the dataset.")
    parser.add_argument("--do-problem", action='store_true', help="Preprocess the dataset.")
    args = parser.parse_args()
    return args
def check_path(args):
    assert os.path.exists("./Data")
    if not os.path.exists(args.log_path):
        os.mkdir(args.log_path)
    if not os.path.exists(args.processed_path):
        os.mkdir(args.processed_path)
def save_args(args,logger):
    save_args_file = os.path.join(args.root_path, "args.txt")
    line = str(args)
    with open(save_args_file, mode="w", encoding="utf-8") as wfp:
        wfp.write(line + "\n")
    logger.info("Args saved in file%s" % save_args_file)
def process(args,logger):
    '''
    文章去重复处理
    :param args:
    :param logger:
    :return:
    '''
    if args.do_pre:
        raw_file = os.path.join(args.processed_path, 'NLP_Corpus.txt')
        save_json = os.path.join(args.processed_path, "NLP_Corpus_Person_Article.json")
        if not os.path.exists(raw_file):
            combine(args.raw_path,raw_file)
            logger.info("File saved in %s"%raw_file)
        args.raw_file = raw_file
        if not os.path.exists(save_json):
            get_person_filter(raw_file,save_json)
            logger.info("File saved in %s" % save_json)
        save_markov_file = os.path.join(args.processed_path, "markov_data.json")
        if not os.path.exists(save_markov_file):
            get_days_items(save_json,args.topic_words_file,save_markov_file)
            logger.info("File saved in %s" % save_markov_file)
def process_markov(args,logger):
    if args.do_problem:
        save_markov_file = os.path.join(args.processed_path, "markov_data.json")
        time_val_list,np_mat1 = get_hot_times_rate(save_markov_file)
        save_fig = os.path.join(args.log_path, "pic_hot_rate.png")
        if not os.path.exists(save_fig):
            draw_hot_rate(time_val_list,np_mat1,save_fig)
            logger.info("Picture save in file:%s"%save_fig)
        # 构建矩阵
        time_val_list,np_mat2 = get_month_rate(save_markov_file)
        save_results_file = os.path.join(args.log_path, "results.txt")
        with open(save_results_file,mode='w',encoding='utf-8') as wfp:
            rights_nums, all_nums = get_markov_trans_mat(np_mat1)
            line1 = '时间间隔为月份时候的正确结果为:(%d,%d)'%(rights_nums,all_nums)
            logger.info(line1)
            wfp.write(line1)
            rights_nums, all_nums = get_markov_trans_mat(np_mat2)
            line2 = '时间间隔为天时候的正确结果为:(%d,%d)' % (rights_nums, all_nums)
            wfp.write(line2)
            logger.info(line2)
            logger.info("Results save in file:%s" % save_fig)
def main():
    args = parse_args()
    logger = Logger(args)
    check_path(args)
    process(args, logger)
    process_markov(args,logger)
if __name__ == '__main__':
    main()