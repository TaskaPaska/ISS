# ISS
Analyzing ISS Data for Useless Insights

Overview
The objective of this project is to analyze ISS Satellite data. The project will involve gathering publicly available data from an API, performing data engineering tasks, and conducting exploratory data analysis. The following sections provide a detailed description of each step involved in the project. 
Data Collection 
The main(and only, really) API for ingesting data from is located at "Where the ISS at?" REST API. Data must be collected so that information about the satellite for every second is stored(refer to the rate limiting section on the API website). 
Specifications 
Since we’re sending requests over the network to retrieve data, it can easily take over 1 second for the entire process(send request, receive response, do stuff before sending another request). To avoid having missing time gaps due to this, there are 2(and possibly more) approaches to the solution:
Real-Time Solution: This solution is for those more proficient in Python but also ensures that we have real-time data available. Use async libraries and functionality for sending requests every second to avoid waiting for other stuff to finish.
Near Real-Time Solution: This is a simpler-to-implement solution with the downside of not having real-time data for the satellite, but somewhat close to it. Instead of having a forever-running process to download the data every second, create a cron job that runs every minute and downloads the data for every second of the past minute. 
 
Data Extraction 
The API will be used to extract all 13 fields providing data regarding the satellite.
Specifications 
Entire data in its raw format must be stored somewhere, in a data lake, data warehouse or both, as preferred. You can only then extract specific fields and variables for specific use cases and analytics from the project’s data infrastructure as in future new specifications may arise and having everything on the project’s end will be crucial. NOTE: avoid having many small files, for example 10 000 JSON files. Consider storing data in hive-partitioned parquet files(What is Apache Parquet? (databricks.com), python - How to write a partitioned Parquet file using Pandas - Stack Overflow) vs organized JSON/CSV and choose the best for the case.

Data Analysis
Since we’re constantly retrieving data, a filesystem and an OLTP database is most suitable for storing it first. However, for our (useless) analysis, an OLAP one is the best, such as Google BigQuery. The data must be periodically ingested to BigQuery from the existing sources to enable fast ad-hoc analysis, for example daily during midnight.
Write SQL queries to perform some analysis on the ISS location history. For example, you could find out(AI-generated ideas, pls do whatever u want dis not important):
The average, minimum, and maximum altitude and velocity of the ISS over a given time period.
The number of times the ISS was visible or eclipsed by the Earth over a given time period.
The countries or regions that the ISS passed over or was closest to over a given time period.
The distance traveled by the ISS over a given time period.



Data Backfill
There must be a scheduled process that runs every 1 hour to find missing time gaps in the database and retrieve the missing data for them(backfill).
Specifications 
The backfill process should be orchestrated using Apache Airflow. Having a DAG that runs every hour and checks for the missing data and downloads it would be sufficient. The missing data should be written straight to the OLTP database, only written to files or a separate table for error logging if the transaction fails for whatever reason.
Infrastructure 
The project will be hosted locally and on Google Cloud Platform. 
Here is one architecture example:
● Local filesystem - serving as a data lake for storing raw files
● PostgreSQL(local) - transactional database for storing the data and periodically ingesting missing data(trust me you will have a lot of those since this is your first project, ideally you would only want either the filesystem or an OLTP for storing the raw data, OLTP preferred when there is a web-application inserting/updating the transactional data, we don’t have such but just for the sake of practice use both still)
● Apache Airflow - automation and scheduling 
● Cron Job/Python Process - downloading the data
● Google BigQuery - OLAP warehouse for ad-hoc analysis

There can be some improvements made but we will discuss them later after having a first working implementation.
