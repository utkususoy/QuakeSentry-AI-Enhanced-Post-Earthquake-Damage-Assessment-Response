import torch.nn as nn
from transformers import RobertaModel, BertTokenizer, BertForSequenceClassification, AutoModel, BertModel

class PoolerClassifier(nn.Module):

    def __init__(self, dropout=0.5):
        super().__init__()
        # self.roberta_model = RobertaModel.from_pretrained('roberta-base')
        self.roberta_model = BertModel.from_pretrained('dbmdz/bert-base-turkish-128k-uncased')
        self.dropout = nn.Dropout(dropout)
        self.classifier_layer = nn.Linear(768, 3)
        

    def forward(self, input_ids, attention_mask):
        _, pooled_output = self.roberta_model(input_ids=input_ids, attention_mask=attention_mask, return_dict=False)
    #    pooler = raw_output['pooler_output']    # Shape is [batch_size, 768]
        dropout_output = self.dropout(pooled_output)
        output = self.classifier_layer(dropout_output)  # Shape is [batch_size, 7]
        return output
