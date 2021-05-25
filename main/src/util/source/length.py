import matplotlib.pyplot as plt
import matplotlib
import json
import csv

from tqdm import tqdm

def length_calculate(save_json,save_length_file):
    with open(save_json,mode="r",encoding="utf-8") as rfp:
        outData = json.load(rfp)
    length_list = []
    for item in tqdm(outData, desc="length calculating"):
        value = item['article']
        idx = item['id']
        length = len(value)
        length_list.append([idx,length])
    length_list = sorted(length_list,key=lambda x:x[1],reverse=True)
    with open(save_length_file,mode="w",encoding="utf-8") as wfp:
        # writer = csv.writer(wfp)
        for item in length_list:
            wfp.write(str(item[0])+","+str(item[1])+"\n")
            #writer.writerow(item)

def draw_length(save_length_file,save_fig):
    matplotlib.rc("font", family='MicroSoft YaHei', weight="bold")
    all_data = []
    with open(save_length_file,mode="r",encoding="utf-8") as rfp:
        reader = csv.reader(rfp)
        for item in reader:
            idx = item[0]
            length = int(item[1])
            all_data.append([idx,length])
    zero_items = 0
    zero_ten_items = 0
    ten_fifty_items = 0
    fifty_hundred_items = 0
    hundred_fifty_items = 0
    hundredFifty_hundredSeventy_items = 0
    hundredSeventy_Twohundred_items = 0
    up_items = 0
    for item in all_data:
        if item[1] == 0:
            zero_items += 1
        elif item[1]<10:
            zero_ten_items += 1
        elif item[1]<50:
            ten_fifty_items += 1
        elif item[1]<100:
            fifty_hundred_items += 1
        elif item[1]<150:
            hundred_fifty_items += 1
        elif item[1]<170:
            hundredFifty_hundredSeventy_items += 1
        elif item[1]<220:
            hundredSeventy_Twohundred_items += 1
        else:
            up_items += 1
    # 画出对应的条形统计图
    y_title = ["0", "1-10", "10-50", "50-100", "100-150", "150-170","170-220","220以上"]
    freq_list = [zero_items, zero_ten_items, ten_fifty_items, fifty_hundred_items,
                 hundred_fifty_items, hundredFifty_hundredSeventy_items, hundredSeventy_Twohundred_items,
                 up_items]
    length = len(freq_list)
    x_list = range(length)
    # 中文乱码的处理
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False

    plt.figure(figsize=(10, 6))
    plt.bar(x_list, freq_list, align='center', alpha=0.8, width=0.8)
    plt.xticks(x_list, y_title)
    plt.xlabel('文本长度')
    plt.ylabel('数量')
    plt.title('微博评论文本长度数据分布')
    # 给条形图添加数据标注
    for x, y in enumerate(freq_list):
        plt.text(x-0.2, y + 1, "%s" % y)
    plt.savefig(save_fig)
    plt.close()
