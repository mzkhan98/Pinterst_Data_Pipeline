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

The batch processing layer runs queries on the entire data set, allowing for metrics that depend on historical data, such as the most popular categories for a certain demographic or age group. Kafka dumps the data to an S3 bucket, and Spark is used for data cleaning and feature computation. Pinball, an orchestration tool similar to Airflow, triggers Spark jobs, which are not run automatically. At the end of the batch layer, the data is stored in Apache HBase. Presto is used to run ad hoc queries on raw historical data.

Between 2015 -2017 Pinterest User base grew from 100 million to 175 million, number of running experiements doubled. This rapid growth meant that the legacy system which used Hadoop and Hive could not process data in time for daily deadline, which meant teams could not make data driven decisions quickly. 

## Data Ingest


Before sending any data to Apache Kafka, Zookeeper and the Kafka Broker needs to be run first and then a Kafka topic can be created.Next I had to create a Kafka Producer so that data from the API could be sent to the topic.

Data is sent to the Kafka topic by running both the project_pin_API.py and user_posting_emulation.py  in the Pinterest_App folder.The first task was to create a Kafka topic to send data to. 

The pipeline is then divided into 2 parts which are independent of each other and they are:

Real-time processing 
Batch processing 

Finally I created two identical consumer pipelines; a batch processing pipeline and a streaming pipeline. At this point both pipelines were required to extract data from the kafka topic




Both sections process the same data (loaded from the same Kafka topic), but the first part processes data in real-time while the second part processes the data by scheduling using Apache Airflow.
Moreover, the database used to store the processed data is different for each part as it is shown in the above diagram.
Prometheus is used to monitor the databases while Grafana is used to display graphs of what are being monitored (if applicable).


he data used during this project was obtained by scrapping the Pinterest website (not part of this project but an example of the scrapper can be found at the following link: https://github.com/BlairMar/Pinterest-webscraping-project).