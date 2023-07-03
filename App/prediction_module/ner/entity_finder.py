import torch
from transformers import BertTokenizerFast
from .bert_ner_module import BertModel
from copy import deepcopy
import re, string, json
from unidecode import unidecode

### tokenizer = BertTokenizerFast.from_pretrained('dbmdz/bert-base-turkish-cased')  # singlethon

class EntityFinder:

    def __init__(self) -> None:
        self.base_model = BertModel()
        self.base_model.load_state_dict(torch.load("prediction_module/ner/model/lower_complete_dataset_epoch_14_loss_0.05510063871773548.pt", map_location=torch.device('cpu')))
        self.model = deepcopy(self.base_model).eval()
        self.ids_to_labels = {0: 'B-LOCATION', 1: 'I-ORGANIZATION', 2: 'B-ORGANIZATION', 3: 'I-LOCATION', 4: 'B-PERSON', 5: 'I-PERSON', 6: 'O'}
        self.tokenizer = BertTokenizerFast.from_pretrained('dbmdz/bert-base-turkish-cased')
        with open("prediction_module/nlp_sources/Gazzeters/il_ilce_mahalle_gazetters_v4.json", encoding="utf-8") as f:
            self.gazzeters = json.load(f)
        self.province_list = list(self.gazzeters.keys())
        self.town_dict_list, self.neighbour_list = self.load_gazzeters_lists()
        self.short_word_dict = self.load_short_words_dict()

    def load_short_words_dict(self):
        short_word_dict = dict()

        # Short-cut Words
        with open("prediction_module/nlp_sources/Shortcuts_Words/short_words.txt", "r", encoding= 'utf-8') as f:
            for line in f:
                splitted = line.split()
                short_word_dict[splitted[0]] = str(splitted[1])
        return short_word_dict

    def load_gazzeters_lists(self):
        town_list = []
        neignours_list = []

        for pro_name, towns in self.gazzeters.items():
            for town_name, neignours in towns.items():
                neignours_list += neignours
            town_list.append(towns)
        return town_list, neignours_list    

    def evaluate_one_text(self, model, sentence):

        # use_cuda = torch.cuda.is_available()
        # device = torch.device("cuda" if use_cuda else "cpu")

        # if use_cuda:
        #     model = model.cuda()
    ###    model.eval()
    #    ids_to_labels = {0: 'B-PERSON', 1: 'I-ORGANIZATION', 2: 'I-PERSON', 3: 'B-ORGANIZATION', 4: 'I-LOCATION', 5: 'O', 6: 'B-LOCATION'}
    ###    ids_to_labels = {0: 'B-LOCATION', 1: 'I-ORGANIZATION', 2: 'B-ORGANIZATION', 3: 'I-LOCATION', 4: 'B-PERSON', 5: 'I-PERSON', 6: 'O'}
        text = self.tokenizer(sentence, padding='max_length', max_length = 283, truncation=True, return_tensors="pt")

        mask = text['attention_mask']
        input_id = text['input_ids']
        label_ids = torch.Tensor(self.align_word_ids(sentence)).unsqueeze(0)
        
        with torch.no_grad():
            logits = model(input_id, mask, None)
            logits_clean = logits[0][label_ids != -100]

            predictions = logits_clean.argmax(dim=1).tolist()
            prediction_label = [self.ids_to_labels[i] for i in predictions]
            
            return prediction_label

    def align_word_ids(self, texts, label_all_tokens = False):
    
        tokenized_inputs = self.tokenizer(texts, padding='max_length', max_length=283, truncation=True)

        word_ids = tokenized_inputs.word_ids()

        previous_word_idx = None
        label_ids = []

        for word_idx in word_ids:

            if word_idx is None:
                label_ids.append(-100)

            elif word_idx != previous_word_idx:
                try:
                    label_ids.append(1)
                except:
                    label_ids.append(-100)
            else:
                try:
                    label_ids.append(1 if label_all_tokens else -100)
                except:
                    label_ids.append(-100)
            previous_word_idx = word_idx

        return label_ids

    def location_extraction(self, sentence, entity_labels):
        puncs = string.punctuation # can be extendable 
        locations = []
        location_w_list = []
        o_counter = 0
        for char in puncs:
            sentence = sentence.replace(char, " "+char+" ")

        tokens = sentence.split()

        for token, label in zip(tokens, entity_labels):
            if label == "O":
                o_counter += 1
                continue
            if label == "B-LOCATION" or label == "I-LOCATION":
                # print("BBBB")
                # if o_counter > 4 and location_w_list:
                #     print("AAAAAAA")
                #     print(token)
                    
                #     locations.append(" ".join(location_w_list))
                #     location_w_list = []

                #     o_counter = 0
                    
                location_w_list.append(token)

    ##### DENEME    location = " ".join(location_w_list)
        
        # if location not in locations and location != "":
        #     locations.append(location)

    ##### DENEME    return location
        return location_w_list
    
    def fix_short_words(self, word, shortest_words):

        if word in shortest_words.keys():
            return shortest_words[word]
        else:
            return word
        
    
    
    def address_filter(self, address_tokens):
        province_ = ""
        town_ = ""
        town_identifier = ["ilce", "ilçe"]
        
        street_ = ""
        avenue_ = ""
        boulevard_ = ""
        nei_hood_ = ""
        
        next_search = []

        def separate_word_compound_with_number(text):
            pattern = r'(\D+)(\d+)'
            separated_text = re.sub(pattern, r'\1 \2 ', text)
            return separated_text.strip()
        
        address_tokens = separate_word_compound_with_number(" ".join(address_tokens)).split()
        address_tokens = [unidecode(self.fix_short_words(token_.lower().strip(), shortest_words=self.short_word_dict)) for token_ in address_tokens]
        address_tokens = re.sub(r'[^\w\s]', '', (" ".join(list(filter(lambda x: x.strip(), [re.sub(r'[^\w\s]', ' ', t) for t in address_tokens]))))).split()
        
        custom_entity_tags = ["O" for i in range(len(address_tokens)) ]

        for idx, token in enumerate(address_tokens):
            if "mahalle" in token:
                custom_entity_tags[idx] = "mah-i"
            if "ilce" in token:
                custom_entity_tags[idx] = "ilce"
            if "sokak" in token:
                custom_entity_tags[idx] = "sok-i"
            if "cadde" in token:
                custom_entity_tags[idx] = "cad-i"
            if "bulvar" in token:
                custom_entity_tags[idx] = "blv-i"
            if "apartman" in token:
                custom_entity_tags[idx] = "apt"

        

        def town_neighbour_extractor(town_neighbour_dict):
            neighbour_list = []
            for k,v in town_neighbour_dict.items():
                neighbour_list += v
            return neighbour_list

        def get_key_by_value(dict, value):
            for k, v in dict.items():
                if value in v:
                    return k

            # If value is not found in the dictionary, return None
            return None
        
        def find_missing_province(town_name, neibour_name):
            missing_province = ""
            if town_name:
                for prov, town_dict in self.gazzeters.items():
                    try:
                        if town_name in list(town_dict.keys()):
                            missing_province = prov
                            
                        if neibour_name and neibour_name in self.gazzeters[prov][town_name]:
                            return missing_province
                    except Exception as e:
                        continue
            return missing_province

        # Case 3: No Province (il) and No Town (ilçe)
        def neighbourhood_finder(address_tokens, next_search, brute_flag = True):
            # find Neighbourhood (Mahalle)
            
            # if brute_flag:
            #     next_search = self.neighbour_list
            neighbour_name = ""

            neigbour_identifier_flag = False
            neigbour_entity_flag = False
            
            prev_token = ""
            prev_prev_token = ""
            
            index_list = []

            def united_sparate_neighbour_search(token, gazzeters_, p_token="", pp_token=""):
                
                finding_type = ""
                valid_token = ""
                address_flag = False
                multi_token_neighbor = []
                
            #    multi_token_neighbor = [[neighbors for neighbors in neighbors_street if len(neighbors.split())>1] for neighbors_street in gazzeters_]
                # multi_token_neighbor = [[token, token], [token, token, token], [], ...]
                if gazzeters_ is dict:
                    for neighbors_street in gazzeters_:
                        for neighbors in neighbors_street:
                            if len(neighbors.split())>1:
                                multi_token_neighbor.append(neighbors)
                else:
                    multi_token_neighbor = [neighbors_street for neighbors_street in gazzeters_ if len(neighbors_street.split()) > 1]

                if pp_token: # token, p_token, pp_token exist
                    finding_type = "pp"

                    # Case 1: Sentence: Separate, Gazzeters: United
                    if pp_token+" "+p_token+" "+token in gazzeters_:
                        valid_token = pp_token+" "+p_token+" "+token
                    elif pp_token+" "+p_token+token in gazzeters_:
                        valid_token = pp_token+" "+p_token+token
                    elif pp_token+p_token+" "+token in gazzeters_:
                        valid_token = pp_token+p_token+" "+token
                    elif pp_token+p_token+token in gazzeters_:
                        valid_token = pp_token+p_token+token
                    
                    if valid_token:
                        address_flag = True
                    
                if p_token and not address_flag: # token, p_token exist, pp_token not-exist
                    finding_type = "p"

                    if p_token+" "+token in gazzeters_:
                        valid_token = p_token+" "+token
                    elif p_token+token in gazzeters_:
                        valid_token = p_token+token
                    
                    if valid_token:
                        address_flag = True

                if not address_flag: # Only token exist 
                    finding_type = "t"

                    if token in gazzeters_:
                        valid_token = token
                    # Case 2: Sentence: United, Gazzeters: Separate
                    else:
                        for sep_token in multi_token_neighbor:
                            united_token = "".join(sep_token.split())
                            if token == united_token:
                                valid_token = sep_token
                    
                #if valid_token:
                return valid_token, finding_type            

            for idx, token in enumerate(address_tokens):
                
                token = token.lower().strip()
                if check_entity_address_identifier(idx, entity_tokens=custom_entity_tags, identifier_type="mah-i"):
                    try:
                        if "mahalle" in token:
                            custom_entity_tags[idx] = "mah-i"
                            neigbour_identifier_flag = True

                            if prev_token and neighbour_name == "":
                                neighbour_name = prev_token
                                custom_entity_tags[idx-1] = "mah"
                            break
                        
                        valid_token, search_type = united_sparate_neighbour_search(token=token, p_token=prev_token, pp_token=prev_prev_token, gazzeters_=next_search)
                        #yanlış mah yapabiliyor.
                    #    if token in next_search: #if search_type==t
                        if search_type == 't' and valid_token:
                            index_list = []
                            index_list.append(idx)
                            # custom_entity_tags[idx] = "mah"
                            neighbour_name = valid_token
                            neigbour_entity_flag = True
                        
                    #    if prev_token+" "+token in next_search: #if search_type==pp
                        if search_type == 'p' and valid_token:
                            # custom_entity_tags[idx] = "mah"
                            # custom_entity_tags[idx-1] = "mah"
                            index_list = []
                            index_list.append(idx)
                            index_list.append(idx-1)
                            neighbour_name = valid_token
                            neigbour_entity_flag = True
                            #break
                    #    if prev_prev_token+" "+prev_token+" "+token in next_search:
                        #TODO: 2li ve 3lü mahalle bulursa ilce ve il bulmaya çalış.
                        if search_type == 'pp' and valid_token:
                            # custom_entity_tags[idx] = "mah"
                            # custom_entity_tags[idx-1] = "mah"
                            # custom_entity_tags[idx-2] = "mah"
                            index_list = []
                            index_list.append(idx)
                            index_list.append(idx-1)
                            index_list.append(idx-2)
                            neighbour_name = valid_token
                            neigbour_entity_flag = True
                            break
                       
                        if ((neigbour_entity_flag and neigbour_identifier_flag) or (idx == (len(address_tokens)-1))):
                            print("hereeee")
                            for index in index_list:
                                custom_entity_tags[index] = "mah"
                            break
                    except Exception as e:
                        print(e)
                        

                    if prev_token:
                        prev_prev_token = prev_token
                    prev_token = token

                
            return neighbour_name

        # check token's right after token is address identifier
        def check_entity_address_identifier(token_idx, entity_tokens, identifier_type=""):
            
            identifiers_ = [idnt_ for idnt_ in ["ilce", "mah-i", "cad-i", "sok-i", "blv-i", "apt"] if idnt_ != identifier_type]

            if token_idx < len(entity_tokens)-1:
                if entity_tokens[token_idx+1] in identifiers_:
                    return False
            return True



        # find Province (İl)
        for idx, token in enumerate(address_tokens):
            token = token.lower().strip()
            try:
                if check_entity_address_identifier(idx, entity_tokens=custom_entity_tags):  
                    next_search = self.gazzeters[token]
                    custom_entity_tags[idx] = "il"
                    province_ = token 
                    break
            except Exception as e:
                province_ = ""
                next_search = self.town_dict_list
        
        # find Town (İlçe)
        for idx, token in enumerate(address_tokens):
            token = token.lower().strip()
            try:
                if check_entity_address_identifier(idx, entity_tokens=custom_entity_tags, identifier_type="ilce"):
                    # Find Town(ilçe) based on exist Province(il)
                    if province_:
                        next_search = next_search[token]
                        custom_entity_tags[idx] = "ilce"
                        town_ = token
                        break 
                    else:
                        for town_dict in self.town_dict_list:
                            for town_n in town_dict.keys():
                                if token == town_n:
                                    next_search = town_dict[town_n]
                                    custom_entity_tags[idx] = "ilce"
                                    town_ = town_n
                                    break
                            if town_:
                                break
                # break
            except Exception as e:
                town_ = ""
            #Son kapatılan.
            # # # if town_ == "":
            # # #     next_search = self.neighbour_list

        # Case 1: yes Province (il), No Town (ilçe), yes Neighbour (Mahalle)
        # Check Neighbourhood (Mahalle) then try to find Town (ilçe) through Neighbourhood (Mahalle)
        if town_ == "" and province_:
            nei_hood_ = neighbourhood_finder(address_tokens=address_tokens, next_search=town_neighbour_extractor(self.gazzeters[province_]), brute_flag=False)
            town_ = get_key_by_value(self.gazzeters[province_], nei_hood_)
            if town_:
                next_search = self.gazzeters[province_][town_]
        
        # Find Neighbourhood (Mahalle) through Town-Neighbour (İl-Mahalle) dictionary
        if nei_hood_ == "":
            brute_flag_ = True
            if town_:
                brute_flag_ = False
            elif not town_ and not province_:
                next_search = self.neighbour_list
            nei_hood_ = neighbourhood_finder(address_tokens=address_tokens, next_search=next_search, brute_flag=brute_flag_)

        # # # Case 2: No Province (il), No Town (ilçe), yes Neighbour (Mahalle)
        # # # if there is no Province (il) and Town (ilçe) existance
        # # # if town_ == "" and province_ == "" :
        # # #     for idx, token in enumerate(address_tokens):
        # # #         for town_dict in self.town_dict_list:
        # # #             for town_n, neighbor_l in town_dict.items():
        # # #             #    print(town_n)
        # # #                 if token in neighbor_l:
        # # #                     next_search = town_dict[town_n]
        # # #                     custom_entity_tags[idx] = "ilce"
        # # #                     town_ = town_n     

        # Missing Province (il) through Town (ilçe) and Neighbourhood (Mahalle)
        if province_ == "":
            province_ = find_missing_province(town_name=town_, neibour_name=nei_hood_)

        def small_address_identifier_generator(tokens, entities):
            for idx, (token, entity) in enumerate(zip(tokens, entities)):
                if "sokak" in token:
                     entities[idx] = "sok-i"
                if "cadde" in token:
                     entities[idx] = "cad-i"
                if "bulvar" in token:
                     entities[idx] = "blv-i"
            return entities
                
        # find Street (Sokak)
        def small_address_indentifier_finder(tokens, entities, identifier_token):
            address_list = ""
            prev_token = ""
            prev_prev_token = ""
            nearest_address_indentity = ""
            neighbor_idx = ""

            adress_itentifier_dict = {
                "sokak": "sok",
                "cadde": "cad",
                "bulvar": "blv"
            }
            
            for idx, (token, entity) in enumerate(zip(tokens, entities)):
                if identifier_token in token:
                #    entities[idx] = identifier_token                   
                    if nearest_address_indentity:
                        address_list = address_tokens[nearest_address_indentity+1:idx]
                        for entity_index in range(nearest_address_indentity+1, idx):
                            entities[entity_index] = adress_itentifier_dict[identifier_token]
                        return " ".join(address_list), entities
                    else:
                        if neighbor_idx != "":
                            address = " ".join(address_tokens[neighbor_idx+1:idx])
                            for entity_index in range(neighbor_idx+1, idx):
                                entities[entity_index] = adress_itentifier_dict[identifier_token]
                        else:
                            address = prev_token
                            entities[idx-1] = adress_itentifier_dict[identifier_token]
                        return address, entities

                if entity == "mah-i" or entity == "il" or entity == "ilce" or entity == "cad-i" or entity == "sok-i" or entity == "blv-i": # generic olunca extend et sok cad bulv için.
                    nearest_address_indentity = idx

                if entity == "mah":
                    neighbor_idx = idx

                if prev_token:
                    prev_prev_token = prev_token
                prev_token = token

            return address_list, entities
        
        # Set all small address identifier tokens (Street, Avenue, Bulvar)
        custom_entity_tags = small_address_identifier_generator(tokens=address_tokens, entities=custom_entity_tags)

        # find Street (Sokak)
        street_, custom_entity_tags = small_address_indentifier_finder(tokens=address_tokens, entities=custom_entity_tags, identifier_token="sokak")
        # find Avenue (Cadde)
        avenue_, custom_entity_tags = small_address_indentifier_finder(tokens=address_tokens, entities=custom_entity_tags, identifier_token="cadde")
        # find Boulevard (Bulvar)
        boulevard_, custom_entity_tags = small_address_indentifier_finder(tokens=address_tokens, entities=custom_entity_tags, identifier_token="bulvar")

        def digit_detector(address):
            temp_address = []
            for token in address.split():
                if token.isdigit():
                    token = token + "."
                temp_address.append(token)
            return " ".join(temp_address)
        
        def valid_address_compiler(province, town, neighbor, street, avenue, boulevard):

            neighbor = (neighbor and neighbor + " Mahallesi, ") or ""
            street = (street and street + " Sokak, ") or ""
            avenue = (avenue and avenue + " Caddesi, ") or ""
            boulevard = (boulevard and boulevard + " Bulvarı, ") or ""
            town = (town and town + ", ") or ""

            return f"{neighbor}{street}{avenue}{boulevard}{town}{province}".strip()

        if town_ is None:
            town_ = ""

        print(address_tokens)
        print(custom_entity_tags)

        print(f"İl: {province_}")
        print(f"İlçe: {town_}")
        print(f"Mahalle: {nei_hood_}")
        print(f"Sokak: {digit_detector(street_)}")
        print(f"Cadde: {digit_detector(avenue_)}")
        print(f"Bulvar: {digit_detector(boulevard_)}")

        not_none_count = sum(var is not "" for var in [province_, town_, nei_hood_, street_, avenue_, boulevard_])

        open_address = valid_address_compiler(province=province_.strip(), town=town_.strip(), neighbor=nei_hood_.strip(), street=digit_detector(street_).strip(), avenue=digit_detector(avenue_).strip(), boulevard=digit_detector(boulevard_).strip())
        if open_address == "":
            print("heeee")
            return None
        if not_none_count >= 2:
            # Do your work here
            print("Work is being done!")
            return open_address
        else:
            return ""

    def location_finder(self, sentence):
    ###    model = BertModel()
    ###    model.load_state_dict(torch.load("ner\model\complete_dataset_epoch_4_loss_0.058543760829415675.pt"))
    #     sentence = """Alsancak Mahallesi Ayasofya caddesi 221.Sokak Kırıkhan/HATAY
    # Mustafa YONCA 
    # 0535 049 3779"""
    #    sentence = "Arzan Sokak"
        # sentence = """Bahçelievler Mah 501 Sokak No 2 KIRIKHAN/HATAY abi buraya da lütfen"""
    #     sentence = """Hatay /Antakya
    # Öğretmenler evi karşısı Selvi apartmanı 
    # Sesler geliyor halen yaşayanlar var
    # Çok acil ...yardım"""
    # sentence = odabaşı mahallesi kayuka sokak akademi sitesi blok+
        pred_res = self.evaluate_one_text(model=self.model, sentence=sentence)
        locations = self.location_extraction(sentence, pred_res)
#        print(locations)
        return locations
    #    print(pred_res)

        

    # if __name__ == "__main__":
    #     location_finder()