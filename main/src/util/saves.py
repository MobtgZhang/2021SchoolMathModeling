import csv
import json
from .preprocess import save_xlsx_file
def save_result_xlsx(save_json,first_xlsx_file,document_max_result_file,topics_results_file):
    dictID2topicID = {}
    with open(document_max_result_file,mode="r",encoding="utf-8") as rfp:
        reader = csv.reader(rfp)
        for item in reader:
            idx = item[0]
            topic_id = item[1]
            if idx not in dictID2topicID:
                dictID2topicID[idx] = topic_id
    topicID2name = {}
    with open(topics_results_file,mode="r",encoding="utf-8") as rfp:
        reader = csv.reader(rfp)
        for item in reader:
            topic_id = item[0]
            topic_name = item[1]
            if idx not in topicID2name:
                topicID2name[topic_id] = topic_name
    with open(save_json, mode="r", encoding="utf-8") as rfp:
        raw_data = json.load(rfp)
    length = len(raw_data)
    for k in range(length):
        idx = raw_data[k]['id']
        if idx not in dictID2topicID:
            raw_data[k]['topic'] = ''
            raw_data[k]['topic_id'] = ""
        else:
            raw_data[k]['topic'] = topicID2name[dictID2topicID[idx]]
            raw_data[k]['topic_id'] = dictID2topicID[idx]
    save_xlsx_file(raw_data,first_xlsx_file)

