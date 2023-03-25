from kafka import KafkaProducer

# Create a Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Send a message to a topic
producer.send('ZainsPinterestData', b'Hello, Kafka!')

# Flush the producer to ensure all messages are sent
producer.flush()