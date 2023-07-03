from pydantic import BaseModel

class DamagedContent():
    def __init__(self, tweet, processed_tweet, label, address, geo_code, valid_address ):
        self.raw_tweet = tweet,
        self.social_processed_tweet = processed_tweet,
        self.label = str(label),
        self.address = address,
        self.geo_code = geo_code
        self.valid_address = valid_address

    def content_to_dict(self):
        return {
            "raw_tweet" : self.raw_tweet,
            "social_processed_tweet": self.social_processed_tweet,
            "label": self.label,
            "address": self.address,
            "geo_code": self.geo_code,
            "valid_address": self.valid_address
        }

class Tweet(BaseModel):
    tweet_uuid_ : str
    tweet : str
    processed_tweet : str
    label : str
    address : str
    geo_code : str
    valid_address : str
    
class UpdateTweetType(Tweet):
    tweet_uuid_: str
    label: str