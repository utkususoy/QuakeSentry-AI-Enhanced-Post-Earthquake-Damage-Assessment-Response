import torch
from transformers import RobertaTokenizer, BertTokenizer, BertForSequenceClassification
import numpy as np

labels_dict = {'none':0,
          'violent':1,
          'weak':2
          }
# Initialize the tokenizer
# tokenizer = RobertaTokenizer.from_pretrained("roberta-base")
tokenizer = BertTokenizer.from_pretrained("dbmdz/bert-base-turkish-128k-uncased")          

class TransformerDataset(torch.utils.data.Dataset):

    def __init__(self, texts, targets, tokenizer=tokenizer, seq_len=282):        
        self.texts = texts
        self.targets = targets # (targets and [labels_dict[target] for target in targets]) or None
        self.tokenizer = tokenizer
        self.seq_len = seq_len
    
    def __len__(self):
        """Returns the length of dataset."""
        return len(self.texts)
    
    def __getitem__(self, idx):
        """
        For a given item index, return a dictionary of encoded information        
        """        
        text = str(self.texts[idx]) 
        
        tokenized = self.tokenizer(
            text,            
            max_length = self.seq_len,                                
            padding = "max_length",     # Pad to the specified max_length. 
            truncation = True,          # Truncate to the specified max_length. 
            add_special_tokens = True,  # Whether to insert [CLS], [SEP], <s>, etc.   
            return_attention_mask = True            
        )     
        
        return {"ids": torch.tensor(tokenized["input_ids"], dtype=torch.long),
                "masks": torch.tensor(tokenized["attention_mask"], dtype=torch.long),
                "target": self.targets # (self.targets and torch.tensor(self.targets[idx], dtype=torch.float)) or None
               }

    # def __init__(self, texts, targets, max_seq_len=512):
        
    #     self.texts = [tokenizer(text, padding='max_length', max_length = max_seq_len, 
    #                             add_special_tokens = True, return_tensors="pt",
    #                             truncation=True) for text in texts],
    #     self.labels = [labels_dict[target] for target in targets]
        

    # def __len__(self):
    #     return len(self.texts)

    # def __getitem__(self, idx):
    #     """
    #     For a given item index, return a dictionary of encoded information        
    #     """  
    #     batch_X = str(self.texts[idx])
    #     batch_y = np.array(self.labels[idx])

    #     return batch_X, batch_y




    #    targets = np.array(self.labels[idx])

        # tokenized = self.tokenizer(
        #     text, 
        #     max_length = self.max_seq_len,
        #     padding = "max_length",     # Pad to the specified max_length.
        #     truncation = True,          # Truncate to the specified max_length.
        #     add_special_tokens = True,  # Whether to insert [CLS], [SEP], <s>, etc.
        #     return_attention_mask = True
        # )

        # return {
        #     "ids": torch.tensor(tokenized["input_ids"], dtype=torch.long),
        #     "masks": torch.tensor(tokenized["attention_mask"], dtype=torch.long),
        #     "target": torch.tensor(self.labels[idx], dtype=torch.long)
        # }

# def main_test():
#     num_list = [0, 1, 2, 3, 4, 5]
#     print(num_list)
#     obj_ = TransformerDataset(num_list)
#     print(obj_)

# if __name__ == '__main__':
#     main_test()
