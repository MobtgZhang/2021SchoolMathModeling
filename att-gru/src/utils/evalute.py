import datetime
import json

import torch

def list_to_device(tp_list, device):
    for index in range(len(tp_list)):
        tp_list[index] = [tp_list[index][0].to(device), tp_list[index][1].to(device)]
    return tp_list
def get_length(x):
    length_list = []
    for index in range(len(x)):
        length_list.append(x[index].size(1))
    return length_list
def evalute(model, test_loader,device):
    model.eval()
    correct = 0
    correct_a = 0
    correct_b = 0
    for step, (x, y) in enumerate(test_loader):
        x = list_to_device(x, device)
        week_index, word_index = y[0], y[1]
        pred_spans, pred_words = model(x)
        pred_spans = pred_spans.cpu().detach()
        pred_words = pred_words.cpu().detach()
        tp_week_index = torch.argmax(pred_spans,dim=1)
        tp_word_index = torch.argmax(pred_words, dim=1)
        v_a = (tp_week_index == week_index)
        v_b = (tp_word_index == word_index)
        v_c = v_a & v_b
        correct += v_c.sum()
        correct_a += v_a.sum()
        correct_b += v_b.sum()
    length = len(test_loader.dataset)
    correct = correct / length
    correct_a = correct_a / length
    correct_b = correct_b / length
    return correct,correct_a,correct_b
def change_to_vec(inputs,dictionary,device):
    days = []
    docs_list = []
    max_length = 0
    for k in range(len(inputs)):
        doc = inputs[k][1]
        year, month, day = inputs[k][0].split('/')
        year, month, day = int(year),int(month),int(day)
        if k == 0:
            week_index = datetime.timedelta(days=0)
            time0 = datetime.date(year,month,day)
        else:
            time1 = datetime.date(year,month,day)
            week_index = time1 - time0
        days.append(week_index.days)
        docuement = [dictionary[word] for word in doc]
        if max_length<len(docuement):
            max_length = len(docuement)
        docs_list.append(docuement)
    bt_size = len(inputs)
    words_id = torch.zeros(size=(bt_size,max_length),dtype=torch.long).to(device)
    days_id = torch.zeros(size=(bt_size,), dtype=torch.long).to(device)
    for k in range(bt_size):
        item = docs_list[k]
        days_id[k] = days[k]
        for j in range(len(item)):
            words_id[k,j] = item[j]
    return [[days_id,words_id]]
def save_best_results(model,test_loader,dictionary,device,save_file):
    all_data = []
    for item in test_loader.dataset.dataset:
        inputs = item['input']
        targets = item['target']

        mod_input = change_to_vec(inputs,dictionary,device)

        year,month,day = inputs[0][0].split('/')
        year, month, day = int(year),int(month),int(day)
        time0 = datetime.date(year,month,day)
        pred_spans, pred_words  = model(mod_input)
        tp_week_index = torch.argmax(pred_spans).cpu().detach().numpy().tolist()
        tp_word_index = torch.argmax(pred_words).cpu().detach().numpy().tolist()
        pr_word = dictionary[tp_word_index]
        pr_week = time0 + datetime.timedelta(days=tp_week_index)
        time1 = str(pr_week.year) + '/'+str(pr_week.month) + '/'+str(pr_week.day)
        predict = [time1,pr_word]
        tp_dict = {
            'input': inputs,
            'target': targets,
            'predict':predict
        }
        all_data.append(tp_dict)
    with open(save_file,mode='w',encoding='utf-8') as wfp:
        json.dump(all_data,wfp)
