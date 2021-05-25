import argparse
import os
import json

from src.data import Logger
from src.util import combine,preprocess
from src.util import create_filter_documents
from src.model import LDA,BM25HF_KMeans
from src.util import topics_draw,topics_draw_pie
from src.util import make_comments_times,make_trans_dis_times,make_comments_times_onlymonth,make_trans_dis_times_bymonth
from src.util import load_max_topics,get_time_to_topics,make_topics_times
from src.util import save_result_xlsx,save_xlsx_file
from src.util import get_person_filter


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-path",type=str,default="./Data",help="preprocess raw data path.")
    parser.add_argument("--processed-path", type=str, default="./processed", help="processed path.")
    parser.add_argument("--log-path", type=str, default="./log", help="Topic model.")
    parser.add_argument("--stop-words-file", type=str, default="./stopwords.txt", help="stopwords file.")
    parser.add_argument("--do-pre", action='store_true', help="Whether to preprocess the model.")
    parser.add_argument("--do-sentiment", action='store_true', help="Sentiment series of statistical data.")
    parser.add_argument("--model-name", type=str, default="lda",
                        help="Topic model.")
    parser.add_argument("--num-topics", type=int, default=50,
                        help="Number topics of lda model")
    parser.add_argument("--num-words", type=int, default=12,
                        help="Number of words.")
    parser.add_argument("--max-iter", type=int, default=350,
                        help="Number of words.")
    parser.add_argument("--alpha", type=float, default=0.25,
                        help="alpha of lda.")
    parser.add_argument("--beta", type=float, default=0.1,
                        help="alpha of lda.")
    parser.add_argument("--by-month", action='store_true',help="draw month of time series.")
    parser.add_argument("--batch-size", type=int, default=50, help="batch size of time series.")
    parser.add_argument("--length-size", type=int, default=30, help="picture size of time series.")
    parser.add_argument("--do-first", action='store_true', help="The first item of the math modeling problem.")
    parser.add_argument("--do-second", action='store_true', help="The second item of the math modeling problem.")
    parser.add_argument("--do-third", action='store_true', help="The third item of the math modeling problem.")
    args = parser.parse_args()
    return args
def save_args(args,logger):
    save_args_file = os.path.join(args.root_path, "args.txt")
    line = str(args)
    with open(save_args_file, mode="w", encoding="utf-8") as wfp:
        wfp.write(line + "\n")
    logger.info("Args saved in file%s" % save_args_file)
def check_path(args):
    assert os.path.exists("./Data")
    if not os.path.exists(args.log_path):
        os.mkdir(args.log_path)
    if not os.path.exists(args.processed_path):
        os.mkdir(args.processed_path)
def preprocess_main(args,logger):
    if args.do_pre:
        raw_file = os.path.join(args.processed_path,'NLP_Corpus.txt')
        save_json = os.path.join(args.processed_path,"NLP_Corpus.json")
        save_csv = os.path.join(args.processed_path, "NLP_Corpus.csv")
        save_xlsx = os.path.join(args.processed_path, "NLP_Corpus.xlsx")
        if not os.path.exists(raw_file):
            combine(logger,args.raw_path,raw_file)
        args.raw_file = raw_file
        if not os.path.exists(save_json):
            preprocess(logger, args, "all")
        if not os.path.exists(save_csv):
            preprocess(logger, args, "json")
        if not os.path.exists(save_xlsx):
            preprocess(logger, args, "xlsx")
        logger.info("Preprocessing has done!")
def first_problem(args,logger):
    if args.do_first:
        # 准备数据集
        save_json = os.path.join(args.processed_path, "NLP_Corpus.json")
        saved_filter_file = os.path.join(args.processed_path, "NLP_Corpus_Filter.json")
        if not os.path.exists(saved_filter_file):
            create_filter_documents(save_json, saved_filter_file, args.stop_words_file, jieba=True, singleWords=False)
            logger.info("The document saved in file:%s" % saved_filter_file)
        # 对22万个文档进行聚类分析处理
        root_path = os.path.join(args.log_path, 'first', args.model_name)
        if not os.path.exists(root_path):
            os.makedirs(root_path)
        args.root_path = root_path
        if args.model_name.lower() == 'lda':
            save_lda_model_file = os.path.join(root_path, "NLP_Corpus_lda.mdl")
            if not os.path.exists(save_lda_model_file):
                lda_model = LDA(args)
                lda_model.run()
                lda_model.save(logger,
                               lda_model.topic_result_file,
                               lda_model.document_max_result_file)
            else:
                lda_model = LDA(args)
                lda_model.load(save_lda_model_file)
            # 可视化处理
            # 主题数量分布图
            save_fig = os.path.join(root_path, 'pic_lda_%s_%d.png' % ("first", args.num_topics))
            document_max_result_file = os.path.join(args.root_path, "document_max_topics_results.csv")
            if not os.path.exists(save_fig):
                topics_draw(document_max_result_file,save_fig,'first')
                logger.info("Pictures saved in path:%s"%root_path)
            save_pie_path = os.path.join(root_path,'pie_pictures')
            csv_save_file = os.path.join(root_path, 'topics_results.csv')
            if not os.path.exists(save_pie_path):
                topics_draw_pie(csv_save_file,save_pie_path,'lda')
                logger.info("Pictures saved in path:%s" % root_path)
            # 将最大值保存为xlsx文件
            first_xlsx_file = os.path.join(root_path, 'first_result.xlsx')
            document_max_result_file = os.path.join(root_path, "document_max_topics_results.csv")
            topics_results_file = os.path.join(root_path, "topics_results.csv")
            if not os.path.exists(first_xlsx_file):
                save_result_xlsx(save_json,first_xlsx_file,document_max_result_file,topics_results_file)
                logger.info("Saved in path:%s" % first_xlsx_file)
        else:
            raise Exception("Unknown model name:%s" % args.model_name)
        # 保存参数
        save_args(args, logger)
        # 保存logger
        logger.save_log()
def second_problem(args,logger):
    if args.do_second:
        # 准备数据集
        save_json = os.path.join(args.processed_path, "NLP_Corpus.json")
        saved_filter_person_file = os.path.join(args.processed_path, "NLP_Corpus_Persons_Article.json")
        if not os.path.exists(saved_filter_person_file):
            get_person_filter(save_json,saved_filter_person_file,stop_words_file= args.stop_words_file)
            logger.info("The document saved in file:%s" % saved_filter_person_file)
        # 计算人物的热度值
        root_path = os.path.join(args.log_path, 'second','bm25hf')
        if not os.path.exists(root_path):
            os.makedirs(root_path)
        args.root_path = root_path
        save_topics_file = os.path.join(root_path,'topics_results.csv')
        save_results_file = os.path.join(root_path,'document_max_topics_results.csv')
        if not os.path.exists(save_topics_file) or not os.path.exists(save_results_file):
            model = BM25HF_KMeans(args)
            model.run()
            model.save_topics(logger,save_topics_file,save_results_file)
        # 画出统计图
        # 主题数量分布图
        save_fig = os.path.join(root_path, 'pic_bm25hf_%s_%d.png' % ("second", args.num_topics))
        document_max_result_file = os.path.join(args.root_path, "document_max_topics_results.csv")
        if not os.path.exists(save_fig):
            topics_draw(document_max_result_file,save_fig, 'second')
            logger.info("Pictures saved in path:%s" % root_path)
        save_pie_path = os.path.join(root_path, 'pie_pictures')
        csv_save_file = os.path.join(root_path, 'topics_results.csv')
        if not os.path.exists(save_pie_path):
            topics_draw_pie(csv_save_file,save_pie_path,'bm25hf')
            logger.info("Pictures saved in path:%s" % root_path)
        # 将最大值保存为xlsx文件
        second_xlsx_file = os.path.join(root_path, 'second_result.xlsx')
        document_max_result_file = os.path.join(root_path, "document_max_topics_results.csv")
        topics_results_file = os.path.join(root_path, "topics_results.csv")
        if not os.path.exists(second_xlsx_file):
            save_result_xlsx(save_json, second_xlsx_file, document_max_result_file, topics_results_file)
            logger.info("Saved in path:%s" % second_xlsx_file)
        # 保存参数
        save_args(args, logger)
        # 保存logger
        logger.save_log()
def get_topics_first(args,name = 'first'):
    save_topic_num_dict_json = os.path.join(args.log_path, name, args.model_name, 'topic_num_dict.json')
    if not os.path.exists(save_topic_num_dict_json):
        first_csv = os.path.join(args.log_path, name, args.model_name, 'document_max_topics_results.csv')
        article_to_topics = load_max_topics(first_csv)
        save_json = os.path.join(args.processed_path, "NLP_Corpus.json")
        all_dict = get_time_to_topics(article_to_topics, save_json)
        with open(save_topic_num_dict_json, mode='w', encoding='utf-8') as wfp:
            json.dump(all_dict, wfp)
    else:
        with open(save_topic_num_dict_json, mode='r', encoding='utf-8') as rfp:
            all_dict = json.load(rfp)
    # 获取最大值并且画出图
    root_path = os.path.join(args.log_path, name, args.model_name,'topics')
    if not os.path.exists(root_path):
        os.mkdir(root_path)
        save_file = os.path.join(args.log_path, name, args.model_name, "topics_results.csv")
        make_topics_times(root_path,save_file,all_dict,name,args.batch_size)
def third_problem(args,logger):
    if args.do_third:
        # comments
        save_json = os.path.join(args.processed_path, "NLP_Corpus.json")
        comments_path = os.path.join(args.log_path,'comments')
        save_fig = os.path.join(comments_path, 'pic_time_comments_month.png')
        if not os.path.exists(save_fig):
            if not os.path.exists(comments_path):
                os.mkdir(comments_path)
            make_comments_times_onlymonth(save_json, save_fig)
            logger.info("Saved in path%s"%save_fig)
            make_comments_times(save_json, comments_path,args.batch_size,args.length_size)
            logger.info("Saved in path%s" % comments_path)
        else:
            pass
        # transmit
        transmits_path = os.path.join(args.log_path, 'transmit')
        save_fig = os.path.join(transmits_path, 'pic_time_transmit_month.png')
        if not os.path.exists(save_fig):
            if not os.path.exists(transmits_path):
                os.mkdir(transmits_path)
            make_trans_dis_times_bymonth(save_json, save_fig,'transmit')
            logger.info("Saved in path%s"%save_fig)
            make_trans_dis_times(save_json, transmits_path, args.batch_size,args.length_size,'transmit')
            logger.info("Saved in path%s"%transmits_path)
        discuss_path = os.path.join(args.log_path, 'discuss')
        save_fig = os.path.join(discuss_path, 'pic_time_discuss_month.png')
        if not os.path.exists(save_fig):
            if not os.path.exists(discuss_path):
                os.mkdir(discuss_path)
            make_trans_dis_times_bymonth(save_json, save_fig,'discuss')
            logger.info("Saved in path%s"%save_fig)
            make_trans_dis_times(save_json, discuss_path, args.batch_size, args.length_size, 'discuss')
            logger.info("Saved in path%s" % discuss_path)
        # 话题分布图
        get_topics_first(args)

def main():
    args = parse_args()
    check_path(args)
    logger = Logger(args)
    preprocess_main(args,logger)
    # 解决第一个问题
    first_problem(args,logger)
    # 解决第二个问题
    second_problem(args,logger)
    # 解决第三个问题
    third_problem(args,logger)

if __name__ == '__main__':
    main()