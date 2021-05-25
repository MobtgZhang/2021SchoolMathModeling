import matplotlib.pyplot as plt
import matplotlib
import json

from tqdm import tqdm

from ...data import Vocabulary

def origin_calculate(save_json,save_orgin_file):
    vocabulary = Vocabulary()
    with open(save_json,mode="r",encoding="utf-8") as rfp:
        outData = json.load(rfp)
    length = len(outData)
    for item in tqdm(outData, desc="word adding"):
        value = item['origin']
        vocabulary.addVocab(value)
    vocabulary.save(save_orgin_file)
    return length
def draw_origin_pie(save_orgin_file,save_fig,topk=6):
    vocabulary = Vocabulary()
    length = 0
    with open(save_orgin_file,mode="r",encoding="utf-8") as rfp:
        rfp.readline()
        for line in rfp:
            index,word,frequency = line.split("\t")
            length += int(frequency)
            vocabulary.addVocabFre(word,int(frequency))
    vocab_list = sorted(vocabulary.word2fre,key=lambda x:x[1],reverse=True)
    labels = [vocab_list[k][0] for k in range(topk)]
    labels.append("其他")
    X = [vocab_list[k][1] for k in range(topk)]
    X.append(length - sum(X))
    matplotlib.rc("font", family='MicroSoft YaHei', weight="bold")
    plt.figure(figsize=(15,10))
    plt.pie(X, labels=labels, autopct='%1.2f%%')  # 画饼图（数据，数据对应的标签，百分数保留两位小数点）
    plt.title("来源")
    plt.savefig(save_fig)
    plt.close()
