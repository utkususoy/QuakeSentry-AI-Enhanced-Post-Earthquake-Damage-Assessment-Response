from kafka import KafkaProducer
import temp_dataloader
# Set up Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9091', 'localhost:9092', 'localhost:9093']  # Kafka broker addresses
)

def produce_raw_tweets(producer: KafkaProducer, tweets: list):

    # Produce messages to topic
    for tweet in tweets:
        message = f"{tweet}".encode('utf-8')  # encode message as bytes
        response = producer.send('raw-tweets', message)  # send message to topic
        result = response.get(timeout=60)
        print(result)
    # Wait for any outstanding messages to be delivered and delivery reports received
    producer.flush()

    # Close producer connection
    producer.close()

if __name__ == "__main__":
    temp_tweets = temp_dataloader.load_temp_data()
    produce_raw_tweets(producer=producer, tweets=temp_tweets)

#TODO:
# mongoda ki hasarlı Son içeriği dataloader_csv'den çıkart öyle tekrar kafkaya ver. 