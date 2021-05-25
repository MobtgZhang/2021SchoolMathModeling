import os
import csv
import matplotlib.pyplot as plt
import matplotlib
def topics_draw(document_max_result_file,save_fig,typeid):
    tmp_topic = {}
    #document_max_result_file = os.path.join(args.root_path, "document_max_topics_results.csv")
    with open(document_max_result_file, mode="r", encoding="utf-8") as rfp:
        reader = csv.reader(rfp)
        for item in reader:
            index = int(item[1])
            if index not in tmp_topic:
                tmp_topic[index] = 1
            else:
                tmp_topic[index] += 1
        tmp_topic = [[item, tmp_topic[item]] for item in tmp_topic]
        tmp_topic = sorted(tmp_topic, key=lambda x: x[0])

    # 画出对应的条形统计图
    y_title = [item[0] for item in tmp_topic]
    freq_list = [item[1] for item in tmp_topic]
    length = len(freq_list)
    x_list = range(length)
    # 中文乱码的处理
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False

    plt.figure(figsize=(12, 6))
    plt.bar(x_list, freq_list, align='center', alpha=0.8, width=0.8)
    plt.xticks(x_list, y_title)
    plt.xlabel('主题索引')
    plt.ylabel('数量')
    plt.title('主题=%d数量分布' % length)
    #root_path = os.path.join(args.log_path, typeid, args.model_name)
    #save_fig = os.path.join(root_path, 'pic_lda_%s_%d.png' % (typeid, length))
    plt.savefig(save_fig)
    plt.close()
def topics_draw_pie(csv_save_file,tp_path,model_name):
    #root_path = os.path.join(args.log_path,name, args.model_name)
    #csv_save_file = os.path.join(root_path,'topics_results.csv')
    all_data = {}
    with open(csv_save_file,mode="r",encoding="utf-8") as rfp:
        reader = csv.reader(rfp)
        for item in reader:
            index = item[0]
            tmp_data  = {}
            data = item[1].split("+")
            for detail in data:
                rate = float(detail.split("*")[0])
                word = "item:%s"%detail.split("*")[1].replace('"','')
                tmp_data[word] = rate*1000
            # other = sum([tmp_data[word] for word in tmp_data])
            # tmp_data['other'] = 1-other
            all_data[index] = tmp_data
    # 画图
    #tp_path = os.path.join(root_path,'pie_pictures')
    if not os.path.exists(tp_path):
        os.mkdir(tp_path)
    for topic in all_data:
        save_pie_fig = os.path.join(tp_path, 'pic_%s_pie_topic_%s.png' % (topic,model_name))
        X = list(all_data[topic].values())
        labels = list(all_data[topic].keys())
        # 中文乱码的处理
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.figure(figsize=(5, 5))
        plt.pie(X, labels=labels, autopct='%1.2f%%')  # 画饼图（数据，数据对应的标签，百分数保留两位小数点）
        plt.title("话题%s成分比重"%topic)
        plt.savefig(save_pie_fig)
        plt.close()
def load_max_topics(filename):
    all_data = {}
    with open(filename,mode="r",encoding='utf-8') as rfp:
        reader = csv.reader(rfp)
        for item in reader:
            index,topic_index = item
            all_data[index] = int(topic_index)
    return all_data
