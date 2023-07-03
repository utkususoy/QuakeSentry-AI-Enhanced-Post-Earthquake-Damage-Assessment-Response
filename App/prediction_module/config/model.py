import uuid

class DamagedContent:
    def __init__(self, tweet, processed_tweet, label, address, geo_code, valid_address):
        self.raw_tweet = tweet,
        self.social_processed_tweet = processed_tweet,
        self.label = str(label),
        self.address = address,
        self.geo_code = geo_code
        self.valid_address = valid_address
        self.uuid_ = str(uuid.uuid4())

    def content_to_dict(self):
        return {
            "uuid" : self.uuid_,
            "raw_tweet" : self.raw_tweet,
            "social_processed_tweet": self.social_processed_tweet,
            "label": self.label,
            "address": self.address,
            "geo_code": self.geo_code,
            "valid_address": self.valid_address
        }