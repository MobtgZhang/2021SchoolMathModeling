import numpy as np
import datetime
import torch
def vectorize(data, word_dict):
    """Torchify a single example."""

    # Index words
    inputs_list = data['input']
    targets_list = data['target']

    inputs = []
    for k in range(len(inputs_list)):
        year,month,day = inputs_list[k][0].split('/')
        year, month, day = int(year),int(month),int(day)
        if k == 0:
            week_index = datetime.timedelta(days=0)
            time0 = datetime.date(year,month,day)
        else:
            time1 = datetime.date(year,month,day)
            week_index = time1-time0
        tp_list = [word_dict[w] for w in inputs_list[k][1]]
        inputs.append([week_index.days,tp_list])

    year, month, day = targets_list[0].split('/')
    year, month, day = int(year), int(month), int(day)
    time1 = datetime.date(year, month, day)
    week_index = time1 - time0
    targets = [week_index.days,word_dict[targets_list[1]]]
    return {'input':inputs,'target':targets,'<PAD>':word_dict['<PAD>']}
def batchify(batch):
    """Gather a batch of individual examples into one batch."""

    PAD_ID = batch[0]['<PAD>']
    inputs_list = [ex['input'] for ex in batch]
    max_length_list = []
    for docs in inputs_list:
        max_length = max([len(doc[1]) for doc in docs])
        max_length_list.append(max_length)
    inputs = []
    for index,docs in enumerate(inputs_list):
        bat_size = len(docs)
        tp_vecs = torch.zeros((bat_size,max_length_list[index]),dtype=torch.long)
        tp_vecs += PAD_ID
        for k,doc in enumerate(docs):
            for j,word in enumerate(doc[1]):
                tp_vecs[k,j] = word
        tp_list = [doc[0] for doc in docs]
        tp_list = torch.tensor(tp_list,dtype=torch.long)
        inputs.append([tp_list,tp_vecs])
    week_index_list = torch.tensor([ex['target'][0] for ex in batch],dtype=torch.long)
    word_index_list = torch.tensor([ex['target'][1] for ex in batch],dtype=torch.long)
    targets = (week_index_list,word_index_list)
    return inputs,targets
def batchify_test(batch):
    PAD_ID = batch[0]['<PAD>']
    inputs_list = [ex['input'] for ex in batch]
    targets = [ex['target'] for ex in batch]
    max_length_list = []
    for docs in inputs_list:
        max_length = max([len(doc) for doc in docs])
        max_length_list.append(max_length)
    inputs = []
    for index, docs in enumerate(inputs_list):
        bat_size = len(docs)
        tp_vecs = torch.zeros((bat_size, max_length_list[index]), dtype=torch.long)
        tp_vecs += PAD_ID
        for k, doc in enumerate(docs):
            for j, word in enumerate(doc):
                tp_vecs[k, j] = word
        inputs.append(tp_vecs)
    return inputs, targets