import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as mdate
import os
from data import get_date

def draw_hot_rate(time_val_list,np_mat,save_fig):
    all_data = {}
    for time1,value in zip(time_val_list,np_mat):
        year,month,day = time1.split('/')
        year_str = year + '/'+month + '/01'
        if year_str not in all_data:
            all_data[year_str] = []
            all_data[year_str].append(value)
        else:
            all_data[year_str].append(value)

    all_data = [[key,sum(value)/len(value)] for key,value in all_data.items()]
    all_data = sorted(all_data,key=lambda x:get_date(x))

    data_list = [item[1] for item in all_data]
    time_list = [item[0] for item in all_data]

    time_list = pd.DatetimeIndex([item for item in time_list])
    length_size = 30
    title = "热度值变化图"
    x_label = "时间"
    y_label = "热度值"

    matplotlib.rc("font", family='MicroSoft YaHei', weight="bold")
    # 创建一个画布
    fig = plt.figure(figsize=(length_size, 9))
    # 在画布上添加一个子视图
    ax = plt.subplot(111)
    # 这里很重要  需要 将 x轴的刻度 进行格式化
    ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m'))
    # 为X轴添加刻度
    plt.xticks(time_list, rotation=45)
    # 画折线
    ax.plot(time_list, data_list, color='r')
    # 设置标题
    ax.set_title(title)
    # 设置 x y 轴名称
    ax.set_xlabel(x_label, fontsize=20)
    ax.set_ylabel(y_label, fontsize=20)
    plt.savefig(save_fig)
    plt.show()
    plt.close()