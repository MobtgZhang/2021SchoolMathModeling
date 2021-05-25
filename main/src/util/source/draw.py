import matplotlib.pyplot as plt
def draw_frequency(dictWords,save_freq_person,length,title,x_label,y_label):
    dictWords = sorted(dictWords, key=lambda x: x[1], reverse=True)
    # 画出对应的条形统计图
    y_title = [item[0] for item in dictWords[:length]]
    freq_list = [item[1] for item in dictWords[:length]]
    length = len(freq_list)
    x_list = range(length)
    # 中文乱码的处理
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False

    plt.figure(figsize=(30, 6))
    plt.bar(x_list, freq_list, align='center', alpha=0.8, width=0.8)
    plt.xticks(x_list, y_title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.savefig(save_freq_person)
    plt.close()
