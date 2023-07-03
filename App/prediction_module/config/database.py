import pymongo
import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

class DamagedIdentificationDB:
    def __init__(self, app=None):
        db_uri = "mongodb://localhost:27017/"
        db_name = "DamagedBuildingsDB"
        self.client = pymongo.MongoClient(db_uri)
        self.db = self.client[db_name] 
        self.damaged_collection = self.get_collection(collection_name="TezDemoDB") #Demo Only.
    
    # def init_app(self, app):
    #     # db_uri = app.config.get('MONGODB_URI')
    #     # db_name = app.config.get('MONGODB_NAME')
        
    
    def get_collection(self, collection_name: str = "Maras_DamagedTweets_1_v2"):
        return self.db[collection_name]
    
    def insert_record(self, damaged_content_ins):
        payloads = damaged_content_ins.content_to_dict()
        self.damaged_collection.insert_one(payloads)
        return payloads

    def fetch_all(self):
        records = self.damaged_collection.find()
        return records