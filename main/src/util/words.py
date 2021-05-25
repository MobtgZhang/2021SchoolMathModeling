import json
import wordcloud
import matplotlib.pyplot as plt


from ..data import Vocabulary

def get_words(filename):
    with open(filename,mode="r",encoding="utf-8") as rfp:
        rfp.readline()
        all_words = []
        for line in rfp:
            index,word,freq = line.split()
            data_tp = [int(index),word,int(freq)]
            all_words.append(data_tp)
        return all_words
def save_words(all_words,filename):
    with open(filename, mode="w", encoding="utf-8") as wfp:
        wfp.write("index" + "\t" + "word" + "\t" + "frequency" + "\n")
        for item in all_words:
            wfp.write(str(item[0]) + "\t" + item[1] + "\t" + str(item[2]) + "\n")



def get_vocab_frequency(save_json,save_file):
    vocabulary = Vocabulary()
    with open(save_json, mode="r", encoding="utf-8") as rfp:
        outData = json.load(rfp)
        for item in outData:
            document = item[1]
            for word in document:
                vocabulary.addVocab(word)
    vocabulary.save(save_file,list_sorted=True)
def draw_frequency(vocab_freq_file,freq_file,length):
    dictWords = []
    with open(vocab_freq_file, mode="r", encoding="utf-8") as rfp:
        rfp.readline()
        for line in rfp:
            index,word,freq = line.split()
            dictWords.append([word,int(freq)])

    dictWords = sorted(dictWords,key=lambda x:x[1],reverse=True)
    # 画出对应的条形统计图
    y_title = [item[0] for item in dictWords[:length]]
    freq_list = [item[1] for item in dictWords[:length]]
    length = len(freq_list)
    x_list = range(length)
    # 中文乱码的处理
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False

    plt.figure(figsize=(12, 6))
    plt.bar(x_list, freq_list, align='center', alpha=0.8, width=0.8)
    plt.xticks(x_list, y_title)
    plt.xlabel('词频数目排序')
    plt.ylabel('数量')
    plt.title('Top%d词语数量分布' % length)
    plt.savefig(freq_file)
    plt.close()
def draw_cloud(font_path,vocab_freq_file,save_fig,max_words=200):
    word2freq = {}
    all_words = get_words(vocab_freq_file)
    for item in all_words:
        word2freq[item[1]] = item[2]
    word_cloud = wordcloud.WordCloud(font_path=font_path, max_words=max_words,height=1200,
                             width=2400, background_color='white', repeat=False, mode='RGBA')  # 设置词云图对象属性
    word_cloud.generate_from_frequencies(word2freq)

    plt.imshow(word_cloud.to_image())
    plt.axis("off")
    plt.savefig(save_fig)
    plt.close()
