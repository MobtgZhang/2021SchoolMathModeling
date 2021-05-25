import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as mdate
def draw_times_single(save_fig,data,title,x_label,y_label,length_size):
    time_list,data_list = data
    matplotlib.rc("font", family='MicroSoft YaHei', weight="bold")
    # 创建一个画布
    fig = plt.figure(figsize=(length_size, 9))
    # 在画布上添加一个子视图
    ax = plt.subplot(111)
    # 这里很重要  需要 将 x轴的刻度 进行格式化
    ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d'))
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
    plt.close()
def draw_sentiments_times_single(save_fig,data,title,x_label,y_label,length_size):
    time_list,data_list = data
    matplotlib.rc("font", family='MicroSoft YaHei', weight="bold")
    # 创建一个画布
    fig = plt.figure(figsize=(length_size, 9))
    # 在画布上添加一个子视图
    ax = plt.subplot(111)
    # 这里很重要  需要 将 x轴的刻度 进行格式化
    ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d'))
    # 为X轴添加刻度
    plt.xticks(time_list, rotation=45)
    color_list = ['b' if data_list[k]<0.5 else 'r' for k in range(len(data_list))]
    # 绘制条形图
    rects = plt.bar(range(len(data_list)), data_list,color=color_list)
    plt.xticks(time_list, rotation=45)

    # 在条形图上加标注（水平居中）
    #for rect in rects:
        #height = rect.get_height()
        #plt.text(rect.get_x() + rect.get_width() / 2, height + 0.3, str(height), ha='center')
    # 设置标题
    ax.set_title(title)
    # 设置 x y 轴名称
    ax.set_xlabel(x_label, fontsize=20)
    ax.set_ylabel(y_label, fontsize=20)
    plt.savefig(save_fig)
    plt.close()
