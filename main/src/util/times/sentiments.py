import json
import os
from tqdm import tqdm

from ...data import TimeDataLoader
from .time_utils import draw_times_single

def make_sentiments_times(sentiments_path,save_sentiments_json,batch_size,length_size):
    with open(save_sentiments_json, mode="r", encoding="utf-8") as rfp:
        outData = json.load(rfp)
    ListAll = {}
    for item in tqdm(outData, desc="time process"):
        sentiments = item['sentiments']
        time1 = item['time'].split()[0]
        if time1 not in ListAll:
            ListAll[time1] = [0.5,1]
        else:
            ListAll[time1][0] += sentiments
            ListAll[time1][1] += 1
    for item in ListAll:
        value =  ListAll[item][0]/ListAll[item][1]
        ListAll[item] = value - 0.5
    dataloader = TimeDataLoader(ListAll,batch_size)
    for num in range(len(dataloader)):
        name = 'sentiments'
        save_fig = os.path.join(sentiments_path, 'pic_time_%s%d.png' % (name, num))
        draw_times_single(save_fig,dataloader[num],'情感变化图','日期','评论数量',length_size)