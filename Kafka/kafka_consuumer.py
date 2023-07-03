from kafka import KafkaConsumer

# Set up Kafka consumer
consumer = KafkaConsumer(
    'raw-tweets',  # topic to consume from
    bootstrap_servers=['localhost:9091', 'localhost:9092', 'localhost:9093'],  # Kafka broker addresses
    group_id='my-group',  # consumer group ID
    auto_offset_reset='earliest',  # start consuming from earliest available message
    enable_auto_commit=True  # commit offsets automatically after consuming messages
)

# Continuously poll for new messages
for message in consumer:
    print(f"Received message: {message.value.decode('utf-8')}")