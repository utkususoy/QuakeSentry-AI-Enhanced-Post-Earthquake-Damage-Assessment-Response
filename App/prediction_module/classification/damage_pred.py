from .dataset_initializer import TransformerDataset
from .pooler_classifier import PoolerClassifier
from gensim.utils import tokenize
import pickle, torch, re, string
from copy import deepcopy
from transformers import RobertaTokenizer, BertTokenizer, BertForSequenceClassification

class DamagePredicton:

    def __init__(self, shortest_dict, stop_dict) -> None:
        self.base_model = PoolerClassifier()
        self.base_model.load_state_dict(torch.load("prediction_module/classification/model/base_clean_bert_base_loss_0.49692217177814907.pt", map_location=torch.device('cpu')))
        self.model = deepcopy(self.base_model).eval()
        self.label_dict = {'none':0,
          'violent':1,
          'weak':2
        }
        self.idx_to_label_dict = {
            "0": "none",
            "1": "violent",
            "2": "weak"
        }
        self.tokenizer = BertTokenizer.from_pretrained("dbmdz/bert-base-turkish-128k-uncased")
        self.shortest_words = shortest_dict
        self.stop_words = stop_dict

    # def load_dataset():
    #     #Base-Clean - Test
    #     with open("Datasets\\Preproces_Datasets\\v2_base_clean\\test_dataset\\Xtest_dataset.pickle", mode='rb') as f:
    #         base_clean_Xtest = pickle.load(f)
    #     with open("Datasets\\Preproces_Datasets\\v2_base_clean\\test_dataset\\ytest_dataset.pickle", mode='rb') as f:
    #         base_clean_Ytest = pickle.load(f)

    #     return base_clean_Xtest, base_clean_Ytest.tolist()

    def pred_tweet(val_dataset, model):
        
        with torch.no_grad():
            ids = val_dataset[0]["ids"]
            masks = val_dataset[0]["masks"]
            targets = val_dataset[0]["target"] 
            
            output = model(ids, masks)    # Predictions from 1 batch of data.
            pred_val = torch.argmax(output, dim=1)
            return pred_val[0].item()
        
    def predict(self, model, text, tokenizer):
        text_dict = tokenizer(text, padding='max_length', max_length = 282, truncation=True, return_tensors="pt", add_special_tokens = True, return_attention_mask = True )
    #    use_cuda = torch.cuda.is_available()
        # device = torch.device("cuda" if use_cuda else "cpu")
        # if use_cuda:
        #     model = model.cuda()
        mask = text_dict['attention_mask']
        input_id = text_dict['input_ids'].squeeze(1)
        with torch.no_grad():
            output = model(input_id, mask)
            label_id = output.argmax(dim=1).item()
            return label_id
        
    def clean_tweet(self, sentence):
        # # Remove #Hashtags, @Mentions and Urls
        # re_hashtag_mentions = re.compile(r'(@.\S+)|(#.\S+)|(http\S+)')
        # sentence = re_hashtag_mentions.sub(' ', sentence)
        # sentence = sentence.replace(r'[^\x00-\x7F]+', ' ')

        # seperate unifi words
        #    sentence = unifi_word_separator(sentence)   

        # split sentence into tokens
        tokens = list(tokenize(sentence))

        # prepare regex for char filtering
        re_punc = re.compile('[%s]' % re.escape(string.punctuation))
        tokens = [re_punc.sub('', w) for w in tokens]  #Buna bak!!!!! ' ' --> '' yap!!!!!

        # Convert all letters to small letter.
        tokens = [w.lower() for w in tokens]

        # filter out short tokens
        tokens = [w for w in tokens if len(w) > 2]

        # Remove Stopwords
        tokens = [w for w in tokens if w not in self.stop_words]

        # replace normal-ones with shotcut words
        tokens = [self.fix_short_words(w) for w in tokens]

        return ' '.join(tokens)
    
    def fix_short_words(self, word):

        if word in self.shortest_words.keys():
    #        print(short_word_dict[word])
            return self.shortest_words[word]
        else:
            return word
        
    def batch_prediction(batch_data):
        pass

    def single_prediction(self, model, tokenizer, sentence):
        clean_sentence = self.clean_tweet(sentence)
        val_dataset = TransformerDataset(texts=clean_sentence, targets="none")
        result = self.predict(model, val_dataset.texts, tokenizer)
#        return self.label_dict[result]
        return result
        
    def damage_classifier(self, tweet):
        
    #    x_data, y_data = load_dataset()

    # # #    model = PoolerClassifier()
    # # #    model.load_state_dict(torch.load("classification\\model\\base_clean_bert_base_loss_0.49692217177814907.pt"))

    # # #    model.eval()
    ###    tokenizer = BertTokenizer.from_pretrained("dbmdz/bert-base-turkish-128k-uncased")
    #    print(tweet)
        damage_label = self.single_prediction(self.model, self.tokenizer, tweet)
    #    print(damage_label)
        return damage_label, tweet
        # for i in range(len(y_data)):  batch prediction --- y_data will replace

        #     data_idx = i
        #     if y_data[data_idx] == "violent":
        #         #print(y_data[data_idx])
        #         tokenizer = BertTokenizer.from_pretrained("dbmdz/bert-base-turkish-128k-uncased")
        #         val_dataset = TransformerDataset(texts=x_data[data_idx],
        #                                                 targets="none")
        #         print(val_dataset.texts)
        #         result = predict(model, val_dataset.texts, tokenizer)
        #         print(f"Tweet Text: {x_data[data_idx]}")
        #         print(f"Result Label: {result}" )
        #         print(f"True Label: {labels_dict[y_data[data_idx]]}")
        #         print("\n\n")
    # for i in val_dataset:
    #     print(i)
    #     break
    # print(val_dataset[0]["ids"])


    # and you can call it like this:
    # model.eval()
    # predict(model, text='Christiano Ronaldo scored 2 goals in last Manchester United game')

    