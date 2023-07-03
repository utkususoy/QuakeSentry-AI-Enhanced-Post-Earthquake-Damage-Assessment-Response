# List all Topics, Brokers, Partitions
kafka-topics --bootstrap-server localhost:29092 --describe

# Create Topic
kafka-topics --create --topic <topic-name> --replication-factor 3 --partitions 5 --bootstrap-server localhost:9092

# Delete Topic
kafka-topics --bootstrap-server <broker-host>:<broker-port> --delete --topic <topic-name>
