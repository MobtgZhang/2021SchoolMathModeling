import os
import argparse

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

from src.utils import combine
from src.utils import preprocess,get_person_filter
from src.utils import build_bm25hf,build_dataset,build_time_series
from src.data import Logger,NLPDataset,batchify,build_dict,Dictionary,TimeSaver
from src.utils import build_word_embeddings,evalute,save_best_results
from src.model import AttBiLSTM

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-path", type=str, default="./Data", help="preprocess raw data path.")
    parser.add_argument("--processed-path", type=str, default="./processed", help="processed path.")
    parser.add_argument("--log-path", type=str, default="./log", help="Topic model.")
    parser.add_argument("--stop-words-file", type=str, default="./stopwords.txt", help="stopwords file.")
    parser.add_argument("--time-span", type=int, default=15, help="Time span of the dataset.")
    parser.add_argument("--num-days", type=int, default=5, help="days number of the dataset.")
    parser.add_argument("--num-words", type=int, default=100, help="days number of the dataset.")
    parser.add_argument("--emb-file", type=str, default="", help="Embedding file of the model.")
    parser.add_argument("--batch-size", type=int, default=40, help="batch size of the train dataset.")
    parser.add_argument("--embedding-dim", type=int, default=300, help="embedding_dim for model.")
    parser.add_argument("--hidden-dim", type=int, default=50, help="hidden_dim for model.")
    parser.add_argument("--learning-rate", type=float, default=0.01, help="learning rate for the model.")
    parser.add_argument("--epochs", type=float, default=150, help="training epoches for the model.")
    parser.add_argument("--percentage", type=int, default=0.75, help="percentage of the train dataset.")
    parser.add_argument("--do-pre", action='store_true', help="Whether to preprocess the model.")
    parser.add_argument("--do-train", action='store_true', help="process training the model.")
    args = parser.parse_args()
    return args
def check_path(args):
    assert os.path.exists("./Data")
    if not os.path.exists(args.log_path):
        os.mkdir(args.log_path)
    if not os.path.exists(args.processed_path):
        os.mkdir(args.processed_path)
def preprocess_first_stage(args,logger):
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
        preprocess_second_stage(logger,args)
def preprocess_second_stage(logger,args):
    save_json = os.path.join(args.processed_path, "NLP_Corpus.json")
    saved_filter_person_file = os.path.join(args.processed_path, "NLP_Corpus_Persons_Article.json")
    if not os.path.exists(saved_filter_person_file):
        get_person_filter(save_json, saved_filter_person_file, stop_words_file=args.stop_words_file)
        logger.info("The document saved in file:%s" % saved_filter_person_file)
    save_bm25hf_json = os.path.join(args.processed_path,"bm25hf_mat.json")
    if not os.path.exists(save_bm25hf_json):
        build_bm25hf(saved_filter_person_file,save_bm25hf_json)
        logger.info("The document saved in file:%s" % save_bm25hf_json)
    save_dataset_times_json = os.path.join(args.processed_path,"NLP_Corpus_TimeSeries.json")

    if not os.path.exists(save_dataset_times_json):
        build_time_series(save_bm25hf_json,save_dataset_times_json,args.num_words)
        logger.info("The document saved in file:%s" % save_dataset_times_json)
    save_dataset_path = os.path.join(args.processed_path,"nlp_corpus")
    if not os.path.exists(save_dataset_path):
        if not os.path.exists(save_dataset_path):
            os.mkdir(save_dataset_path)
        build_dataset(save_dataset_times_json,save_dataset_path,
                          time_span=args.time_span,
                          num_days=args.num_days,
                          train_percentage=args.percentage)
        logger.info("The train test file saved in path:%s" % save_dataset_path)
def process_train(args,logger):
    if args.do_train:
        if not os.path.exists(args.log_path):
            os.mkdir(args.log_path)
        # 构建数据集
        train_file = os.path.join(args.processed_path, "nlp_corpus", 'train.json')
        test_file = os.path.join(args.processed_path, "nlp_corpus", 'test.json')
        word_dict = Dictionary()
        build_dict(word_dict,train_file)
        build_dict(word_dict,test_file)
        train_dataset = NLPDataset(train_file, word_dict)
        train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True, collate_fn=batchify)
        # 加载词向量
        if args.emb_file.strip() != "":
            word_embedding = build_word_embeddings(args.emb_file)
        else:
            pass
        # 模型构建
        model = AttBiLSTM(vocab_size=len(word_dict), embedding_dim=args.embedding_dim,
                          hidden_dim=args.hidden_dim, time_span=args.time_span+1)
        lossfn = nn.CrossEntropyLoss()
        optimizer = optim.Adamax(params=model.parameters(), lr=args.learning_rate)
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        model.to(device)

        # 模型训练
        def list_to_device(tp_list, device):
            for index in range(len(tp_list)):
                tp_list[index] = [tp_list[index][0].to(device), tp_list[index][1].to(device)]
            return tp_list

        save_model = os.path.join(args.log_path, 'model.ckpt')
        # 保存字典
        save_dict_file = os.path.join(args.log_path, 'dictionary.json')
        word_dict.save(save_dict_file)
        test_file = os.path.join(args.processed_path, "nlp_corpus", 'test.json')
        test_dataset = NLPDataset(test_file, word_dict)
        test_loader = DataLoader(test_dataset, batch_size=args.batch_size, shuffle=False, collate_fn=batchify)
        train_saver = TimeSaver(args.log_path)
        max_acc = 0
        save_best_json_file = os.path.join(args.log_path,'result.json')
        for epoch in range(args.epochs):
            test_loss = 0
            for step, (x, y) in enumerate(train_loader):
                x = list_to_device(x, device)
                week_index, word_index = y[0].to(device), y[1].to(device)
                model.train()
                pred_spans, pred_words = model(x)

                loss = (lossfn(pred_words, word_index) + lossfn(pred_spans, week_index)) / 2
                test_loss += loss.cpu().data.item()
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            # 模型评价
            test_acc, test_acc_a, test_acc_b = evalute(model, test_loader, device)
            test_loss /= len(train_loader)
            if test_acc > max_acc:
                max_acc = test_acc
                # 保存模型预测的结果
                save_best_results(model,test_loader,word_dict,device,save_best_json_file)
                logger.info("File saved in %s"%save_best_json_file)
            # 保存模型
            train_saver.add(test_acc, test_acc_a, test_acc_b, test_loss)
            torch.save(model, save_model)
            logger.info("loss %0.2f,test acc %0.2f,test acc_a %0.2f,test acc_b %0.2f,epoches %d" %
                        (test_loss, test_acc, test_acc_a, test_acc_b, epoch))
        # 画出模型损失变化图
        train_saver.draw()
        train_saver.save_best()
def main():
    args = parse_args()
    check_path(args)
    logger = Logger(args)
    # 预处理
    preprocess_first_stage(args,logger)
    # 训练以及评价模型
    process_train(args,logger)
if __name__ == '__main__':
    main()
