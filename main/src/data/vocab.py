class Vocabulary:
    def __init__(self,frequency=True):
        self.idx2word = []
        self.word2idx = {}
        self.frequency = frequency
        if frequency:
            self.word2fre = []
    def addVocab(self,word):
        if word not in self.word2idx:
            self.word2idx[word] = len(self.idx2word)
            self.idx2word.append(word)
            if self.frequency:
                self.word2fre.append([word,1])
        else:
            if self.frequency:
                self.word2fre[self.word2idx[word]][1] += 1
    def addVocabFre(self,word,frequency):
        if word not in self.word2idx:
            self.word2idx[word] = len(self.idx2word)
            self.idx2word.append(word)
            self.word2fre.append([word,frequency])
        else:
            self.word2fre[self.word2idx[word]][1] = frequency
    def __getitem__(self, item):
        if type(item) == int:
            pass
        elif type(item) == str:
            pass
        else:
            raise TypeError("Unknown type:%s"%str(type(item)))
    def save(self,filename,list_sorted = False):
        tmp_list = [[self.word2idx[word],word,self.word2fre[self.word2idx[word]][1]] for word in self.word2idx]
        if list_sorted:
            tmp_list = sorted(tmp_list,key=lambda x:x[2],reverse=True)
        with open(filename,mode="w",encoding="utf-8") as wfp:
            wfp.write("index"+"\t"+"word"+"\t"+"frequency"+"\n")
            for word in tmp_list:
                wfp.write(str(word[0]) + "\t"+word[1]+"\t"+str(word[2])+"\n")
    def __len__(self):
        return len(self.word2idx)

