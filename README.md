# Pinterest-data-processing-pipeline

![AiCore](https://img.shields.io/badge/Specialist%20Ai%20%26%20Data-AiCore-orange)


![AiCore - Specialist Ai & Data Educator](https://global-uploads.webflow.com/60b9f2c13b02a6f53378e5ac/61f1595967942c65b274cbb0_Logo%20SVG.svg)


## About the project

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

This project is part of the curriculum of the Data Engineering pathway of **AiCore**.  All the coding scripts were written in Python. The OS used is a Dual-Boot Ubuntu 20.04. The objective of this project is to build a data pipeline as shown in the figure below.

![Data Pipeline - UML Diagram](./images/UML_Diagram_For_Pintrest_Project.jpg)

Between 2015-2017, Pinterest's user base grew from 100 million to 175 million, and the number of running experiments doubled. This rapid growth overwhelmed the legacy data processing system that relied on Hadoop and Hive, resulting in missed daily deadlines and slow decision-making.

The goal of this project was to revamp the data pipelines to meet the following requirements:

1. Extensibility to add new metrics and backfill historical data.
2. Scalability to handle massive amounts of data from a growing user base and experiments.
3. Accuracy in computing and serving metrics on dashboards based on historical and recent data.

### Solution

We designed a data processing system based on the Lambda architecture, with a batch processing layer and a streaming layer that work in parallel. The streaming layer handles real-time data processing, while the batch layer is responsible for historical data processing.

### Streaming Layer

Kafka is used to ingest data from events from the app and programmatic interactions from the API. The streaming layer processes the data as soon as it comes in, and metrics that require real-time monitoring, such as ad clicks and active users, are computed in real-time. Spark Streaming is used for data cleaning and transformations. The processed data is then sent to the MemSQL database, which serves the analytics dashboard, allowing for real-time querying of the data.

### Batch Processing Layer

The batch processing layer runs queries on the entire data set, allowing for metrics that depend on historical data, such as the most popular categories for a certain demographic or age group. Kafka dumps the data to an S3 bucket, and Spark is used for data cleaning and feature computation. Airflow, triggers Spark jobs, which are not run automatically. At the end of the batch layer, the data is stored in Apache HBase. Presto is used to run ad hoc queries on raw historical data.


## Task 1: Data Ingestion- Configuring the API 
To complete this task, I downloaded the Pinterest infrastructure, which included the project API and the user emulation program. I ran both programs simultaneously by executing project_pin_API.py first and then user_posting_emulation.py in the Pinterest_App folder provided to students. I verified that the data was being received in the user posting terminal and that the API was receiving an OK status for each POST request.

## Task 2: Data Ingestion - Consuming data in Kafka

For the first task, I created a Kafka topic by running zookeeper and kafka. The code to do this is as follows:

'''
bin/kafka-topics.sh --create --topic Pinterest_Project --partitions 1 --replication-factor 1 --bootstrap-server localhost:9092
'''
I then created a Kafka Producer using kafka-python to send data from the API to the topic.

Next, I created two identical consumer pipelines: a batch processing pipeline and a streaming pipeline. Both pipelines were required to extract data from the Kafka topic. To create the pipelines, I wrote two Python files - batch_consumer.py for the batch processing pipeline and streaming_consumer.py for the real-time streaming pipeline. I used the python-kafka library to make a consumer that received data from the topic created previously.

'''
from kafka import KafkaConsumer
from json import loads

stream_consumer = KafkaConsumer(
    bootstrap_servers = "localhost:9092",
    value_deserializer = lambda message: loads(message),
    auto_offset_reset = "earliest"
)

stream_consumer.subscribe(topics = "NadirsPinterestData")

for message in stream_consumer:
    print(message)
    print (message.value)
    print(message.topic)
    print(message.timestamp)

'''

To test the pipelines, I ran the API, the user emulation script, and each consumer in separate terminals simultaneously. I verified that both consumers were receiving the data sent to the topic.

### Task 3: Batch Processing - Ingest Data into the Data Lake
To complete this milestone, I created a new AWS S3 bucket to receive data from the Kafka batch processing consumer.

The first thing I did was to create an S3 bucket by using boto3. I did this by creating the following method in my batch consumer python file:

'''
def s3_bucket(self):
        self.s3.create_bucket(Bucket=self.bucket_name,CreateBucketConfiguration={
         'LocationConstraint': 'eu-west-1',})
'''

To extract messages from the consumer in batch_consumer.py, I used Kafka-Python. Once the data was received by the Kafka consumer, I used boto3 to send it to the S3 bucket that I had created.

The data will be kept in S3 for long-term persistent storage, and wait to be processed all at once by Spark batch processing jobs either run periodically by Airflow. 


### Task 4: Batch Processing - Process The Data Using Spark 
