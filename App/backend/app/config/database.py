import pymongo
import json
from bson import ObjectId, json_util

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

class DamagedIdentificationDB:
    def __init__(self):
        db_uri = "mongodb://localhost:27017/"
        db_name = "DamagedBuildingsDB"
        self.client = pymongo.MongoClient(db_uri)
        self.db = self.client[db_name] 
        self.damaged_collection = self.get_collection() #Demo Only. collection_name="TezDemoDB"
    
    # def init_app(self, app):
    #     # db_uri = app.config.get('MONGODB_URI')
    #     # db_name = app.config.get('MONGODB_NAME')
        
    
    def get_collection(self, collection_name: str = "Maras_DamagedTweets_1_v2"):
        return self.db[collection_name]
    
    def insert_record(self, damaged_content_ins):
        payloads = damaged_content_ins.content_to_dict()
        self.damaged_collection.insert_one(payloads)
        return payloads
    
    def parse_json(self, data):
        return json.loads(json_util.dumps(data))

    def fetch_all(self):
        records = []
        cursor_obj = self.damaged_collection.find()
        for doc in cursor_obj:
            records.append(doc)
        return self.parse_json(self.parse_json(records))
    
    def fetch_valid_address(self):
        valid_records = []
        records = self.fetch_all()
    #    print(records)
        for record in records:
            if record["geo_code"] is not None:
                valid_records.append(record)
        return self.parse_json(self.parse_json(valid_records))
    
    def remove_tweet_by_uuid(self, uuid_):
        result = self.damaged_collection.delete_one({"uuid": uuid_})
        print(f"{result.deleted_count} document(s) deleted.")

    def update_tweet_type(self, uuid_, new_label):
        filter = {'uuid': uuid_}  # Replace 'your-record-id' with the ID or unique identifier of the record you want to update
        update = {'$set': {'label': new_label}}
        result = self.damaged_collection.update_one(filter=filter, update=update)
        print(f"{result} document(s) updated.")