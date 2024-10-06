# IoT Real-Time Water Quality Monitoring

## Project Overview

This project implements a real-time water quality monitoring system for Chicago Park District beaches along Lake Michigan. It utilizes IoT sensors to collect hourly measurements of critical water quality parameters such as water temperature, turbidity, and wave height.

### Key Features

- Real-time data ingestion and processing
- Dual implementation: Cloud-based (Google Cloud Platform) and On-premise
- Interactive dashboards for real-time monitoring and historical analysis
- Scalable architecture to handle growing data volumes

## Table of Contents

1. [Technologies Used](#technologies-used)
2. [System Architecture](#system-architecture)
3. [Setup and Installation](#setup-and-installation)
4. [Usage](#usage)
5. [Data Sources](#data-sources)
6. [Contributors](#contributors)

## Technologies Used

### Cloud Implementation
- Apache Kafka
- Google Cloud Pub/Sub
- Google Cloud Dataflow
- Google Cloud Storage
- Google BigQuery
- Elastic Cloud (Elasticsearch)
- Kibana
- Power BI

### On-Premise Implementation
- Apache Kafka
- Apache Spark
- SQL Server
- Elasticsearch
- Kibana
- Power BI

## System Architecture

The project consists of two main data processing pipelines:

1. **Real-Time Monitoring Pipeline**: Provides immediate insights through dashboards visualizing critical water quality metrics.
2. **Long-Term Analysis Pipeline**: Enables researchers to study environmental trends and changes in water quality over time.

### Cloud Architecture Diagram

![Cloud Architecture](https://github.com/youssef5haaban/IoT_Real-Time_Water_Quality_Monitoring/blob/main/assets/images/Cloud_Architecture.png)

### On-Premise Architecture Diagram

![Local Architecture](https://github.com/youssef5haaban/IoT_Real-Time_Water_Quality_Monitoring/blob/main/assets/images/Local_Architecture.png)

## Setup and Installation

### Prerequisites

- Java JDK 11 or higher
- Python 3.8 or higher
- Apache Kafka 2.12
- Apache Spark 4.2
- SQL Server 2019 or higher
- Elasticsearch 8.15.1

### Cloud Setup

1. Set up a Google Cloud Platform account and create a new project.
2. Enable necessary APIs (Pub/Sub, Dataflow, BigQuery, etc.).
3. Set up Kafka and the Pub/Sub connector as described in the [Kafka and Pub/Sub Setup](#) section.
4. Configure Dataflow jobs for data processing.
5. Set up Elastic Cloud through the Google Cloud Marketplace.
6. Configure BigQuery datasets and tables.
7. Set up Power BI and connect it to BigQuery.

### On-Premise Setup

1. Install and configure Apache Kafka.
2. Set up Apache Spark and create the necessary data processing scripts.
3. Install and configure SQL Server.
4. Set up Elasticsearch and Kibana.
5. Configure SSIS packages for ETL operations.
6. Set up Power BI and connect it to your local data sources.

## Usage

[Provide instructions on how to run the system, including any commands or scripts that need to be executed]

## Data Sources

The project uses data from the Chicago Park District's Beach Water Quality - Automated Sensors dataset. The data is accessed through the Socrata Open Data API (SODA).

For more information about the dataset, visit: [Beach Water Quality - Automated Sensors](https://data.cityofchicago.org/Parks-Recreation/Beach-Water-Quality-Automated-Sensors/qmqz-2xku)




## Contributors

- Youssef Shaaban
- Ahmed Osama
- Alhassan Mohamed
- Amr Yasser

Project Mentor: Abdelrahman Elsaied

---

For more detailed information about the project, please refer to the full project documentation.
