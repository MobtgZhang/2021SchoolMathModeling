# 校级数学建模竞赛:题目A解题步骤
## 题目描述: 微博数据信息挖掘
随着计算机和网络技术的快速发展，互联网日渐成为各种信息的载体。人们在上面主动的获取、发布、共享、传播各种观点性信息（包括新闻评论、产品评论、情感微博、网络社区等）。这些观点性内容对于电子商务、舆情控制、信息检索等都具有重要的意义和实用价值。
现有脱敏处理的微博记录22+万条，分别放在22个TXT文件中，每条记录形式如下：
```
<RECORD>
      <id>…</id>
      <article>…</article>
      <discuss>…</discuss>
      <insertTime>…</insertTime>
      <origin>…</origin>
      <person_id>…</person_id>
      <time>…</time>
      <transmit>…</transmit>
</RECORD>
```
以上各字段意义如下：

> id				文章编号
> 
> article		正文
> 
> discuss		评论数目
> 
> insertTime		正文插入时间
> 
> origin			来源
> 
> person_id		所属人物的id
> 
> time			正文发布时间
> 
> transmit		转发

请各组同学完成下列任务：

1. 请对22+万条记录进行聚类分析，并对每一类赋予一个恰当的主题词。
2. 请对所有记录的所属人物进行聚类分析，并对每一类赋予一个恰当的主题词。
3. 对所有记录进行时序分析，挖掘舆情传播的特点和规律。

# 解决方法和思路
+ [主要解决方法(LDA主题模型、BM25HF-KMeans算法)](https://github.com/MobtgZhang/2021SchoolMathModeling/tree/main/main)
+ [基于注意力机制的Att-BiGRU热点词汇预测问题](https://github.com/MobtgZhang/2021SchoolMathModeling/tree/main/att-gru)
+ [基于马尔科夫链热点值预测问题](https://github.com/MobtgZhang/2021SchoolMathModeling/tree/main/markov)


