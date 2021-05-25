# 主程序解决
## 运行环境
+ ubuntu16.04 或ubuntu20.04 (其他版本也可以,建议使用LTS版本)
+ CPU：Intel Corei7-6700HQ CPU
+ Memory:8GB
## 下载数据
在官网上下载对应的数据,将数据放在文件夹`./Data`下面

## 创建虚拟环境
```bash
python -m venv mathmodelenv
source mathmodelenv/bin/activate
```

## 安装对应的包
```bash
pip install -r requirements.txt
```
## 运行方法
首先对数据进行预处理,将数据转化为json文件,数据集的预处理的命令如下所示
```bash
python run.py --do-pre \
--raw-path "./Data" \
--processed-path "./processed" 
```

在文件夹中会生成预处理好的文件:
+ `./processed/NLP_Corpus.json`
+ `./processed/NLP_Corpus.csv`
+ `./processed/NLP_Corpus.xlsx`
+ `./processed/NLP_Corpus.txt`

## 主要问题求解

### 问题一求解
```bash
python run.py --do-first \
--model-name lda \
--num-words 6 \
--num-topics 50 \
--alpha 0.25 \
--beta 0.1 \
--batch-size 50 \
--raw-path "./Data" \
--length-size 30 \
--processed-path "./processed" \
--stop-words "./stopwords.txt" \
--log-path "./log"
```

在文件夹中会生成对应的预处理结果：`./processed/NLP_Corpus_Filter.json`,然后生成对应的结果文件,文件有以下的几个

问题结果文件
+ 对应的主题最大概率词语(10个,最终结果)：`./log/first/lda/topics_results.csv` 
+ 文章对应的主题概率：`./log/first/lda/document_topics_results.csv`
+ 文章对应的最大主题概率(最终结果)：`./log/first/lda/document_max_topics_results.csv`
+ 主题分布统计图：`./log/first/lda/pic_lda_first_<num_topics>.png`
+ 主题饼图：`./log/first/lda/pie_pictures.png`
+ 问题一结果表：`./log/first/lda/first_result.xlsx`

LDA 模型文件
+ `./log/first/lda/NLP_Corpus_lda.mdl`
+ `./log/first/lda/NLP_Corpus_lda.mdl.expElogbeta.npy`
+ `./log/first/lda/NLP_Corpus_lda.mdl.state`

### 问题二求解

```bash
python run.py --do-second \
--model-name bm25hf \
--num_topics 50 \
--num-words 6 \
--max-iter 350 \
--raw-path "./Data" \
--processed-path "./processed" \
--stop-words "./stopwords.txt" \
--log-path "./log"
```

在文件夹中会生成对应的预处理结果：`./processed/NLP_Corpus_Person.json`,然后生成对应的结果文件,文件有以下的几个问题结果文件
+ 对应的主题最大概率词语(10个,最终结果)：`./log/second/bm25hf/topics_results.csv`
+ 用户人物`person_id`对应的最大主题概率(最终结果)：`./log/second/lda/lda_document_max_topics_results.csv`
+ 主题分布统计图：`./log/second/bm25hf/pic_lda_second_<num_topics>.png`
+ 主题饼图：`./log/first/lda/pie_pictures.png`

LDA 模型文件
+ `./log/second/lda/NLP_Corpus_lda.mdl`
+ `./log/second/lda/NLP_Corpus_lda.mdl.expElogbeta.npy`
+ `./log/second/lda/NLP_Corpus_lda.mdl.state`

### 问题三求解
```bash
python run.py --do-third \
--model-name lda \
--batch-size 200 \
--raw-path "./Data" \
--processed-path "./processed" \
--log-path "./log"
```
生成以下文件

+ 主题数量随着时间变化数据文件：`./log/first/topics/topic_num_dict.json`
+ 主题数量随着时间变化图(选取了每天讨论最多的话题)：`./log/first/<first>/pic_time_topics_first_<number>.png`

+ 主题数量随着时间变化数据文件：`./log/second/bm25hf/topics/topic_num_dict.json`
+ 主题数量随着时间变化图(选取了每天讨论最多的话题)：`./log/second/bm25hf/pic_time_topics_second_<number>.png`

+ 文章转发数量变化图：`./log/transmit`
+ 文章讨论数量变化图：`./log/comments`
+ 文章评论数量变化图：`./log/discuss`

## 其他数据生成

生成对应的词频分布图、词云图以及词频文件
```bash
python anaysis.py --do-words-freq \
--processed-path "./processed" \
--log-path "./log" \
--max-words 250 \
--font-path "./YaHei.ttf" \
--top-num 15
```
会生成以下的几个文件:
+ 已排序的文件：`./log/frequency.txt`
+ 词云图：`./log/wordcloud.png`
+ 词频统计图：`./log/wordsfrequency.png`

生成对应评论来源图
```bash
python anaysis.py --do-origin \
--processed-path "./processed" \
--log-path "./log" 
```
生成以下的文件:
+ 排好序的来源统计文件：`./log/origin.txt`
+ 生成图：`./log/origin.png`

生成用户评论数目文件以及用户数目图
```bash
python anaysis.py --do-person \
--processed-path "./processed" \
--log-path "./log" \
--top-num 15 
```
生成以下的文件:
+ 用户评论数量统计文件：`./log/person_freq.txt`
+ 用户评论数量统计图：`./log/person_freq.png`

生成评论(transmit)和讨论(discuss)数量统计图
```bash
python anaysis.py --do-discuss --do-transmit \
--processed-path "./processed" \
--log-path "./log" 
```
生成以下的文件:
+ `/log/transmit_freq_discuss.csv`
+ `/log/transmit_freq_discuss.png`
+ `/log/transmit_freq_distribution_discuss.png`
+ `/log/transmit_freq_distribution_transmit.png`
+ `/log/transmit_freq_transmit.csv`
+ `/log/transmit_freq_transmit.png`

