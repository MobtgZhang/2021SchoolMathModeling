import os
import json
import pandas as pd
from tqdm import tqdm


from .time_utils import draw_times_single
from ...data import TimeDataLoader,DateTime

def make_trans_dis_times(save_json, transmits_path, batch_size,length_size,name):
    with open(save_json, mode="r", encoding="utf-8") as rfp:
        outData = json.load(rfp)
    ListAll = {}
    for item in tqdm(outData, desc="time process"):
        time1 = item['time'].split()[0]
        data = 0 if item[name].strip() =='' else int(item[name])
        if time1 not in ListAll:
            ListAll[time1] = data
        else:
            ListAll[time1] += data
    dataloader = TimeDataLoader(ListAll, batch_size)
    for num in range(len(dataloader)):
        save_fig = os.path.join(transmits_path, 'pic_time_%s%d.png' % (name, num))
        draw_times_single(save_fig, dataloader[num], '%s数量变化图'%name, '日期', '评论数量', length_size)
def make_trans_dis_times_bymonth(save_json,save_fig,name):
    with open(save_json,mode="r",encoding="utf-8") as rfp:
        outData = json.load(rfp)
    ListAll = {}
    for item in tqdm(outData, desc="time process"):
        time1 = item['time'].split()[0]
        data = 0 if item[name].strip() == '' else int(item[name])
        year, month, _ = time1.split('/')
        day = '01'
        time1 = year + '/' + month + '/' + day
        if time1 not in ListAll:
            ListAll[time1] = data
        else:
            ListAll[time1] += data
    length_size = 30
    ListAll = [[item, ListAll[item]] for item in ListAll]
    ListAll = sorted(ListAll, key=lambda x: DateTime(time_str=x[0]))
    time_list = pd.DatetimeIndex([item[0] for item in ListAll])
    data_list = [item[1] for item in ListAll]
    dataset = [time_list,data_list]

    draw_times_single(save_fig, dataset, '%s数量变化图'%name, '日期', '%s数量'%name, length_size)