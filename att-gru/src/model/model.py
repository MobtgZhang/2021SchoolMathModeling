import torch
import torch.nn.functional as F
import torch.nn as nn
class AttBiLSTM(nn.Module):
    def __init__(self,vocab_size,embedding_dim,hidden_dim,time_span):
        super(AttBiLSTM, self).__init__()
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.time_span = time_span
        self.days_emb = nn.Embedding(time_span,embedding_dim)
        self.day_mlp = nn.Linear(embedding_dim,2*hidden_dim,bias=False)
        self.words_emb = nn.Embedding(vocab_size,embedding_dim)
        self.bigru = nn.GRU(input_size=embedding_dim,hidden_size=hidden_dim,batch_first=True,
                            num_layers=1,bidirectional=True)
        self.mlp_words = nn.Linear(in_features=2*hidden_dim,out_features=self.vocab_size)
        self.mlp_spans = nn.Linear(in_features=2*hidden_dim,out_features=self.time_span)
    def forward(self,inputs):
        all_list = []
        for id,(week_id,word_id) in enumerate(inputs):
            emb_weeks = self.days_emb(week_id)
            emb_words = self.words_emb(word_id)
            _,hid = self.bigru(emb_words)
            day_out = self.day_mlp(emb_weeks)
            day_out = day_out.reshape(hid.size())
            day_out = F.relu(day_out)
            hid = torch.cat([day_out,hid],dim=2)
            hid = hid.view(-1,2*self.hidden_dim).unsqueeze(0)
            all_list.append(hid)
        tp_hid = torch.cat(all_list)
        b = tp_hid.bmm(torch.transpose(tp_hid, dim0=1, dim1=2))
        b = torch.tanh(b)
        alpha = F.softmax(b, dim=2)
        atched_seq = alpha.bmm(tp_hid)
        pool_words = torch.mean(self.mlp_words(atched_seq),dim=1)
        pred_words = F.softmax(pool_words,dim=1)
        pool_spans = torch.mean(self.mlp_spans(atched_seq), dim=1)
        pred_spans = F.softmax(pool_spans, dim=1)
        return pred_spans,pred_words
