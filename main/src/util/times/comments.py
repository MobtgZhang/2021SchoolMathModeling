import json
import os
import pandas as pd
from tqdm import tqdm

from .time_utils import draw_times_single
from ...data import TimeDataLoader,DateTime


def make_comments_times(save_json,comments_path,batch_size,length_size):
    with open(save_json,mode="r",encoding="utf-8") as rfp:
        outData = json.load(rfp)
    ListAll = {}
    for item in tqdm(outData, desc="time process"):
        time1 = item['time'].split()[0]
        if time1 not in ListAll:
            ListAll[time1] = 0
        else:
            ListAll[time1] += 1
    dataloader = TimeDataLoader(ListAll,batch_size)
    for num in range(len(dataloader)):
        name = 'comments'
        save_fig = os.path.join(comments_path, 'pic_time_%s%d.png' % (name, num))
        draw_times_single(save_fig,dataloader[num],'评论数量变化图','日期','评论数量',length_size)
def make_comments_times_onlymonth(save_json,save_fig):
    with open(save_json,mode="r",encoding="utf-8") as rfp:
        outData = json.load(rfp)
    ListAll = {}
    for item in tqdm(outData, desc="time process"):
        time2 = item['time'].split()[0]
        year, month, _ = time2.split('/')
        day = '01'
        time1 = year + '/' + month + '/' + day
        if time1 not in ListAll:
            ListAll[time1] = 0
        else:
            ListAll[time1] += 1
    length_size = 30
    ListAll = [[item, ListAll[item]] for item in ListAll]
    ListAll = sorted(ListAll, key=lambda x: DateTime(time_str=x[0]))
    time_list = pd.DatetimeIndex([item[0] for item in ListAll])
    data_list = [item[1] for item in ListAll]
    dataset = [time_list,data_list]
    draw_times_single(save_fig, dataset, '评论数量变化图', '日期', '评论数量', length_size)
