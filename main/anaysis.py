import os
import argparse

from src.data import Logger
from src.util import get_vocab_frequency,draw_frequency,draw_cloud
from src.util import origin_calculate,draw_origin_pie
from src.util import get_person_frequency,draw_person_frequency,draw_person_frequency_peoples
from src.util import get_trans_dis_frequency,draw_trans_dis_frequency,draw_trasmit_frequency_distribution
from src.util import length_calculate,draw_length
from src.util import draw_trasmit_frequency_distribution_lessNum

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--processed-path", type=str, default="./processed", help="processed path.")
    parser.add_argument("--log-path", type=str, default="./log", help="Topic model.")
    parser.add_argument("--font-path", type=str, default="./YaHei.ttf", help="wordcloud font file.")
    parser.add_argument("--max-words", type=int, default=250, help="words number.")
    parser.add_argument("--top-num", type=int, default=15, help="top number.")
    parser.add_argument("--num-words", type=int, default=10,
                        help="Number words of lda.")
    parser.add_argument("--alpha", type=float, default=0.25,
                        help="alpha of lda.")
    parser.add_argument("--beta", type=float, default=0.1,
                        help="alpha of lda.")
    parser.add_argument("--number-size", type=int, default=10,
                        help="number size of data.")
    parser.add_argument("--do-words-freq", action='store_true', help="Word frequency of statistical data.")
    parser.add_argument("--do-less", action='store_true', help="Origin of statistical data.")
    parser.add_argument("--do-origin", action='store_true', help="Origin of statistical data.")
    parser.add_argument("--do-length", action='store_true', help="length of text statistical data.")
    parser.add_argument("--do-person", action='store_true', help="Person series of statistical data.")
    parser.add_argument("--do-discuss", action='store_true', help="Discuss series of statistical data.")
    parser.add_argument("--do-transmit", action='store_true', help="Transmit series of statistical data.")
    parser.add_argument("--cal-same", action='store_true', help="Transmit series of statistical data.")
    args = parser.parse_args()
    return args
def get_text_length(logger,args):
    root_path = args.log_path
    save_length_file = os.path.join(root_path, "length.csv")
    save_json = os.path.join(args.processed_path, "NLP_Corpus.json")
    if not os.path.exists(save_length_file):
        length_calculate(save_json, save_length_file)
        logger.info("saved file:%s" % save_length_file)
    save_length_fig = os.path.join(root_path, "length.png")
    if not os.path.exists(save_length_fig):
        draw_length(save_length_file,save_length_fig)
        logger.info("saved file:%s" % save_length_fig)
def get_freq(logger,args):
    root_path = args.log_path
    save_json = os.path.join(args.processed_path, "NLP_Corpus_Filter.json")
    vocab_freq_file = os.path.join(root_path, 'frequency.txt')
    if not os.path.exists(vocab_freq_file):
        get_vocab_frequency(save_json, vocab_freq_file)
        logger.info("Saved the file:%s" % vocab_freq_file)

    freq_file = os.path.join(root_path, "words_frequency.png")
    if not os.path.exists(freq_file):
        draw_frequency(vocab_freq_file, freq_file, args.top_num)
        logger.info("Saved the file:%s" % freq_file)
    # 绘制成词语云图
    word_cloud_file = os.path.join(root_path, 'words_cloud.png')
    if not os.path.exists(word_cloud_file):
        draw_cloud(args.font_path, vocab_freq_file, save_fig=word_cloud_file, max_words=args.max_words)
        logger.info("Saved the file:%s" % word_cloud_file)
def get_origin(logger,args):
    root_path = args.log_path
    save_orgin_file = os.path.join(root_path, "origin.txt")
    save_json = os.path.join(args.processed_path, "NLP_Corpus.json")
    if not os.path.exists(save_orgin_file):
        origin_calculate(save_json, save_orgin_file)
        logger.info("saved file:%s" % save_orgin_file)
    save_origin_fig = os.path.join(root_path, "origin.png")
    if not os.path.exists(save_origin_fig):
        draw_origin_pie(save_orgin_file,save_origin_fig, topk=6)
        logger.info("saved file:%s" % save_origin_fig)
def get_person(logger,args):
    root_path = args.log_path
    sect = "same" if args.cal_same else "different"
    save_json = os.path.join(args.processed_path, "NLP_Corpus.json")
    person_freq_file = os.path.join(root_path, "person_freq_%s.csv"%sect)
    if not os.path.exists(person_freq_file):
        get_person_frequency(save_json, person_freq_file,cal_same=args.cal_same)
        logger.info("Saved the file:%s" % person_freq_file)
    save_freq_person = os.path.join(root_path, "person_freq_%s.png"%sect)
    if not os.path.exists(save_freq_person):
        draw_person_frequency(person_freq_file, save_freq_person, args.top_num)
    save_freq_person_peoples = os.path.join(root_path, "person_freq_peoples_%s.png"%sect)
    if not os.path.exists(save_freq_person_peoples):
        draw_person_frequency_peoples(person_freq_file, save_freq_person_peoples)
def get_transmit(logger,args,name):
    save_json = os.path.join(args.processed_path, "NLP_Corpus.json")
    root_path = args.log_path
    transmit_freq_file = os.path.join(root_path, "transmit_freq_%s.csv"%name)
    if not os.path.exists(transmit_freq_file):
        get_trans_dis_frequency(save_json, transmit_freq_file,name)
        logger.info("Saved the file:%s" % transmit_freq_file)
    save_freq_transmit_fig = os.path.join(root_path, "transmit_freq_%s.png"%name)
    if not os.path.exists(save_freq_transmit_fig):
        draw_trans_dis_frequency(transmit_freq_file,save_freq_transmit_fig,args.top_num,name)
        logger.info("Saved the file:%s" % save_freq_transmit_fig)
    save_freq_transmit_dis_fig = os.path.join(root_path, "transmit_freq_distribution_%s.png" % name)
    if not os.path.exists(save_freq_transmit_dis_fig):
        draw_trasmit_frequency_distribution(transmit_freq_file,save_freq_transmit_dis_fig,name)
        logger.info("Saved the file:%s" % save_freq_transmit_dis_fig)
def get_transmit_lessten(logger,args,number,name):
    save_json = os.path.join(args.processed_path, "NLP_Corpus.json")
    root_path = args.log_path
    transmit_freq_file = os.path.join(root_path, "num%d_transmit_freq_%s.csv" %(number,name))
    if not os.path.exists(transmit_freq_file):
        get_trans_dis_frequency(save_json, transmit_freq_file, name)
        logger.info("Saved the file:%s" % transmit_freq_file)

    save_freq_transmit_dis_fig = os.path.join(root_path, "transmit_freq_distribution_%s.png" % name)
    if not os.path.exists(save_freq_transmit_dis_fig):
        draw_trasmit_frequency_distribution_lessNum(save_json,transmit_freq_file,number,save_freq_transmit_dis_fig, name)
        logger.info("Saved the file:%s" % save_freq_transmit_dis_fig)
def main(args):
    if args.do_words_freq:
        get_freq(logger,args)
    if args.do_origin:
        get_origin(logger,args)
    if args.do_length:
        get_text_length(logger,args)
    if args.do_transmit:
        get_transmit(logger,args,'transmit')
    if args.do_discuss:
        get_transmit(logger,args,'discuss')
    if args.do_person:
        get_person(logger,args)
    if args.do_less and args.do_transmit:
        get_transmit_lessten(logger,args,args.number_size,'discuss')
    if args.do_less and args.do_transmit:
        get_transmit_lessten(logger,args,args.number_size,'transmit')
if __name__ == '__main__':
    args = parse_args()
    logger = Logger(args)
    main(args)
