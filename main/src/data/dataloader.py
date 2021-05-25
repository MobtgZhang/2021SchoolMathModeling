import math
import pandas as pd
from .times import DateTime
class DataLoader:
    def __init__(self):
        pass
    def __len__(self):
        raise NotImplemented
    def __getitem__(self,item):
        raise NotImplemented
class TimeDataLoader(DataLoader):
    def __init__(self,dataset,batch_size):
        super(TimeDataLoader, self).__init__()
        ListAll = [[item, dataset[item]] for item in dataset]
        ListAll = sorted(ListAll, key=lambda x: DateTime(time_str=x[0]))
        time_list = pd.DatetimeIndex([item[0] for item in ListAll])
        self.time_list = time_list
        self.data_list = [item[1] for item in ListAll]
        self.batch_size = batch_size
        length = len(dataset)
        self.length = math.ceil(length/batch_size)
    def __getitem__(self, item):
        return self.time_list[item*self.batch_size:(item+1)*self.batch_size],\
                self.data_list[item*self.batch_size:(item+1)*self.batch_size]
    def __len__(self):
        return self.length
