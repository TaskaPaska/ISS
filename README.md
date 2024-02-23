# ISS Data Analysis

## Overview

The ISS Data Analysis project aims to gather, process, and analyze data from the International Space Station (ISS) using publicly available APIs. This repository contains code and documentation detailing the process of collecting ISS data, storing it, conducting exploratory data analysis, and performing various analyses to derive insights, albeit possibly useless ones, from the data.

## Data Collection

Data is collected from the "Where the ISS at?" REST API, which provides information about the satellite's location. Two approaches are outlined for data collection:

1. **Real-Time Solution**: Utilizes asynchronous libraries to send requests every second, ensuring real-time data availability.  
2. **Near Real-Time Solution**: Implements a cron job that runs every minute to download data for every second of the past minute.

## Data Extraction

All 13 fields provided by the API are extracted, and the raw data is stored in a data lake or data warehouse. Storing data in hive-partitioned Parquet files is recommended to avoid numerous small files and facilitate future data use cases.

## Data Analysis

Data is stored initially in a filesystem and an OLTP database for efficient retrieval. However, for analysis purposes, data is periodically ingested into Google BigQuery for fast ad-hoc analysis. Sample SQL queries for analysis include:

- Calculating the average, minimum, and maximum altitude and velocity of the ISS over a given time period.  
- Determining the number of times the ISS was visible or eclipsed by the Earth over a given time period.  
- Identifying the countries or regions that the ISS passed over or was closest to over a given time period.  
- Estimating the distance traveled by the ISS over a given time period.

## Data Backfill

A scheduled Apache Airflow process runs every hour to identify missing data gaps in the database and retrieve the necessary data (backfill). The backfill process writes missing data directly to the OLTP database, with error logging implemented for failed transactions.

## Infrastructure

The project is hosted locally and on Google Cloud Platform with the following architecture:

- Local filesystem: Serving as a data lake for storing raw files.  
- PostgreSQL (local): Transactional database for storing data and ingesting missing data.  
- Apache Airflow: Used for automation and scheduling of processes.  
- Cron Job/Python Process: Responsible for downloading data from the API.  
- Google BigQuery: OLAP warehouse for ad-hoc analysis.

## Getting Started

To get started with this project, follow these steps:

1. Clone the repository to your local machine.  
2. Set up the required dependencies as outlined in the documentation.  
3. Configure API keys and connection strings as necessary.  
4. Run the data collection and extraction scripts.  
5. Ingest the data into the appropriate databases.  
6. Execute the provided SQL queries to perform analyses.
