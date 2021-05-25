import re
import jieba

from .lang import Converter

def filter_chinese(sentence: str)-> str:
    '''
    中文的一些预处理
    :param sentence: 输入的句子或文本
    :return:
    '''
    # 去除文本中的url
    sentence = re.sub(r"http\S+", "", sentence)
    # 剔除所有数字
    # decimal_regex = re.compile(r"[^a-zA-Z]\d+")
    # sentence = decimal_regex.sub(r"", sentence)
    # 删除英文字符
    # eng_regex = re.compile(r'[a-zA-z]')
    # sentence = eng_regex.sub(r"", sentence)
    # 删除@用户的字符串
    at_regex = re.compile(r'@[\u4e00-\u9fa5a-zA-Z0-9_-]{2,30}')
    sentence = at_regex.sub(r"", sentence)
    # 删除无意义词语
    sentence = sentence.replace('转发微博',"")
    sentence = sentence.replace('分享图片', "")
    # 去除空格
    space_regex = re.compile(r"\s+")
    sentence = space_regex.sub(r"", sentence)
    # 繁体字转换成简体字
    sentence = Converter('zh-hans').convert(sentence)
    # 去掉所有的标点符号
    # dot_regex = re.compile(r"\p{P}")
    # sentence = dot_regex.sub(r"",sentence)
    # 只保留中文/英文和标点符号,数字
    words = [word for word in sentence if word >= u'\u4e00' and word <= u'\u9fa5' \
             # or word not in ['，', '。', '？', '！', ',', '.', '!', '?','...','、'] \
             # or (word >= u'\u0030' and word <= u'\u0039') \
             or (word >= u'\u0061' and word <= u'\u007a') \
             or (word >= u'\u0041' and word <= u'\u005a')]
    sentence = ''.join(words)
    return sentence.strip().lower()
def jieba_segment(sentence: str,stopword_file,singleWords = True):
    '''
    jieba分词，并去掉停止词
    :param sentence:
    :return:
    '''
    # 停止词过滤
    stopwords_list = [line.rstrip() for line in open(stopword_file,mode="r", encoding="gbk")]
    sentence_list = jieba.cut(sentence)
    if singleWords:
        sentence_list = [w for w in sentence_list if w not in stopwords_list]
    else:
        sentence_list = [w for w in sentence_list if w not in stopwords_list and len(w)>1]
    return sentence_list
