# 基于注意力机制的Att-BiGRU热点词汇预测问题
# 运行环境
+ ubuntu16.04 或ubuntu20.04 (其他版本也可以,建议使用LTS版本)
+ CPU：Intel Corei7-6700HQ CPU
+ Memory:8GB
# 下载数据
在官网上下载对应的数据,将数据放在文件夹`./Data`下面

# 创建虚拟环境
```bash
python -m venv mathmodelenv
source mathmodelenv/bin/activate
```

# 安装对应的包
```bash
pip install -r requirements.txt
```
# 运行方法
## 数据的预处理

首先对数据进行预处理,将数据转化为json文件,数据集的预处理的命令如下所示
```bash
python run.py --do-pre \
--raw-path "./Data" \
--processed-path "./processed" \
--stop-words-file "./stopwords.txt" \
--percentage 0.75
```
## 训练数据

训练过程
```bash
python run.py --do-pre \
--log-path "./log" \
--processed-path "./processed" \
--time-span 15 \
--percentage 0.75 \
--num-words 100 \
--batch-size 40 \
--embedding-dim 300 \
--hidden-dim 50 \
--learning-rate 0.01 \
--epochs 150
```
