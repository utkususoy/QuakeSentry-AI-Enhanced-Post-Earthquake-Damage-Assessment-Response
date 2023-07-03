from ner import entity_finder
from utils.address_converter import get_nominatim_geocode, get_yandex_map_geocoder
from classification.damage_pred import DamagePredicton
from ner.entity_finder import EntityFinder
from kafka import KafkaConsumer, KafkaProducer
import pickle
import json
import time, os, re

from config.database import DamagedIdentificationDB
from config.model import DamagedContent

# Set up Kafka Consumer
consumer = KafkaConsumer(
    'raw-tweets',  # topic to consume from
    bootstrap_servers=['localhost:9091', 'localhost:9092', 'localhost:9093'],  # Kafka broker addresses
    group_id='my-group',  # consumer group ID
    auto_offset_reset='earliest',  # start consuming from earliest available message
    enable_auto_commit=True  # commit offsets automatically after consuming messages
)

# Set uup Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9091', 'localhost:9092', 'localhost:9093'],
    value_serializer=lambda m: json.dumps(m).encode('utf-8')
)

db = DamagedIdentificationDB()

def fix_short_words(word, shortest_words):

        if word in shortest_words.keys():
    #        print(short_word_dict[word])
            return shortest_words[word]
        else:
            return word

def basic_social_network_cleaning(sentence, shortest_dict):
    # Remove #Hashtags, @Mentions and Urls
    re_hashtag_mentions = re.compile(r'(@.\S+)|(#.\S+)|(http\S+)')
    sentence = re_hashtag_mentions.sub(' ', sentence)
    sentence = sentence.replace(r'[^\x00-\x7F]+', ' ')
    # replace normal-ones with shotcut words
    tokens = " ".join([fix_short_words(w.lower().strip(), shortest_words=shortest_dict) for w in sentence.split()])
    return tokens.strip()

def load_preproccess_utils():
        
    short_word_dict = dict()

    # Short-cut Words
    with open("prediction_module/nlp_sources/Shortcuts_Words/short_words.txt", "r", encoding= 'utf-8') as f:
        for line in f:
            splitted = line.split()
            short_word_dict[splitted[0]] = str(splitted[1])
    
    # Stopwords
    stop_words = []
    with open("prediction_module/nlp_sources/Stop_words/stop_words.txt", "r", encoding= 'utf-8') as f:
        for line in f:
            stop_words.append(line.split()[0])

    return short_word_dict, stop_words

if __name__ == "__main__":
#    tweets = fetch_tweets()
    (shortest_dict, stop_dict) = load_preproccess_utils()
    damage_predictor_ = DamagePredicton(shortest_dict, stop_dict)
    location_extractor_ = EntityFinder()
    damaged_tweets = []

    # Continuously poll for new messages
    for message in consumer:
        raw_tweet = message
        print(f"Received message: {message}")
#    damage_tweet = """Bahçelievler Mah 501 Sokak No 2 KIRIKHAN/HATAY duvarlarda çatlak var naber nasılsın okey mi herşey Alsancak Mahallesi Ayasofya caddesi 221.Sokak Kırıkhan/HATAY iyisin gol."""
        message = basic_social_network_cleaning(message.value.decode('utf-8'), shortest_dict)
        damage_label, damage_tweet = damage_predictor_.damage_classifier(message)
        
        if (damage_label == 1 or damage_label == 2) and ("1999 depremi" not in damage_tweet or "99 depremi" not in damage_tweet):
            print(f"Received message: {message}")
            print(f"Label: {damage_predictor_.idx_to_label_dict[str(damage_label)]}")
            geocode_list = []
            # NER Location Extraction
            address = location_extractor_.location_finder(message.lower())
            
            print(f"NER Adress: {address}")
            valid_address = location_extractor_.address_filter(address)
            print(f"Valid Adress: {valid_address}")
            # GEO-Code finding from address
            # for address in addresses:
            #final_address = valid_address or address
            if valid_address is None and address:
                final_address = address[0]
            else:
                final_address = valid_address
            if final_address and len(final_address.split()) > 1:
                try:
                    geocode = get_yandex_map_geocoder(final_address)
                except:
                    pass
            else:
                geocode = None
        #    geocode_list.append(geocode)
            # time.sleep(1)

            print("Producing...")
        
            #TODO classification  sonuçlarını test et.

            content = DamagedContent(address=" ".join(address), geo_code=geocode, label=damage_predictor_.idx_to_label_dict[str(damage_label)], processed_tweet=message, tweet=raw_tweet.value.decode('utf-8'), valid_address=valid_address)
            payload_json = db.insert_record(damaged_content_ins=content)
            # payload_json = {
            #     "raw_tweet": raw_tweet.value.decode('utf-8'),
            #     "social_processed_tweet": message,
            #     "label": damage_predictor_.idx_to_label_dict[str(damage_label)],
            #     "address": " ".join(address), #NER-Adress
            #     "valid_address": valid_address,
            #     "geo_code": geocode
            # }
            print("hereeeeee")

            payload_json.pop("_id")
            print(payload_json)
            response = producer.send("damaged-tweets", value=payload_json)
            result = response.get(timeout=60)
            print(result)
            # Wait for any outstanding messages to be delivered and delivery reports received
            producer.flush()

    # Close producer connection
    producer.close()
    
    # # # address = entity_finder.location_finder(damage_tweet)
    # # # print("heeeee")
    # # # print(address)
#    geocode = get_nominatim_geocode(address)
#    print(geocode)

# payload_json = {
#                 "raw_tweet": raw_tweet.value.decode('utf-8'),
#                 "social_processed_tweet": message,
#                 "label": str(damage_label),
#                 "address": address,
#                 "geo_code": geocode_list
#             }

#             # open the file in append mode
#             with open('only_lower_damaged_data.json', 'a') as f:
#                 # write the dictionary as a JSON-encoded string
#                 json.dump(payload_json, f)
#                 # add a newline character at the end of the line
#                 f.write('\n')