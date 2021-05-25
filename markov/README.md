# 基于马尔科夫链热点值预测问题
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
### 数据的预处理
首先对数据进行预处理,将数据转化为json文件,数据集的预处理的命令如下所示
```bash
python main.py --do-pre \
--raw-path "./Data" \
--processed-path "./processed" \
--log-path "./log" \
-topic-words-file "./topic_words.txt" 
```
会生成以下的文件

+ 马尔科夫链预训练文件:`markov_data.json`
+ 原始材料文件:`NLP_Corpus_Person_Article.json`
+ 合并之后的文件:`NLP_Corpus.txt`

### 问题解决
```bash
python main.py --do-problem 
```
会生成以下的文件
+ 热度趋势图:`pic_hot_rate.png`
+ 结果:`results.txt`
