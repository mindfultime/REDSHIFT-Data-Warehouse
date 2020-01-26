# Data Modeling for Sparkify
## Background 
### Introduction
A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

The project requires to build an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights in what songs their users are listening to.

In order to carry out the project data needs to be loaded from S3 to staging tables on Redshift and execute SQL statements that create the analytics tables from these staging tables.

`Note: Background is based on Udacity Data Engineering Nano degree Program`

## Prerequisites for running the program
The project is built in python 3.x , and AWS Redshift with a 4 node cluster on a dc2.large Redshift cluster

## File Info
### Data Files in S3 bucket:
#### Song_data
The first dataset is a subset of real data from the Million Song Dataset. Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. For example, here are filepaths to two files in this dataset.

```json
song_data/A/B/C/TRABCEI128F424C983.json
song_data/A/A/B/TRAABJL12903CDCF1A.json
```

And below is an example of what a single song file, TRAABJL12903CDCF1A.json, looks like.

```
{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
```

#### Log_data
The second dataset consists of log files in JSON format generated by this event simulator based on the songs in the dataset above. These simulate activity logs from a music streaming app based on specified configurations.

The log files in the dataset you'll be working with are partitioned by year and month. For example, here are filepaths to two files in this dataset.

```
log_data/2018/11/2018-11-12-events.json
log_data/2018/11/2018-11-13-events.json
```
And below is an example of what the data in a log file, 2018-11-12-events.json, looks like.

```	
|    | artist   | auth      | firstName   | gender   |   itemInSession | lastName   |   length | level   | location                          | method   | page     |   registration |   sessionId | song         |   status |            ts | userAgent                                                                                                                  |   userId |
|----|----------|-----------|-------------|----------|-----------------|------------|----------|---------|-----------------------------------|----------|----------|----------------|-------------|--------------|----------|---------------|----------------------------------------------------------------------------------------------------------------------------|----------|
|  0 |          | Logged In | Walter      | M        |               0 | Frye       |  nan     | free    | San Francisco-Oakland-Hayward, CA | GET      | Home     |    1.54092e+12 |          38 |              |      200 | 1541105830796 | "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36" |       39 |
|  1 |          | Logged In | Kaylee      | F        |               0 | Summers    |  nan     | free    | Phoenix-Mesa-Scottsdale, AZ       | GET      | Home     |    1.54034e+12 |         139 |              |      200 | 1541106106796 | "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36"            |        8 |
|  2 | Des'ree  | Logged In | Kaylee      | F        |               1 | Summers    |  246.308 | free    | Phoenix-Mesa-Scottsdale, AZ       | PUT      | NextSong |    1.54034e+12 |         139 | You Gotta Be |      200 | 1541106106796 | "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36"            |        8 |
|  3 |          | Logged In | Kaylee      | F        |               2 | Summers    |  nan     | free    | Phoenix-Mesa-Scottsdale, AZ       | GET      | Upgrade  |    1.54034e+12 |         139 |              |      200 | 1541106132796 | "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36"            |        8 |
|  4 | Mr Oizo  | Logged In | Kaylee      | F        |               3 | Summers    |  144.039 | free    | Phoenix-Mesa-Scottsdale, AZ       | PUT      | NextSong |    1.54034e+12 |         139 | Flat 55      |      200 | 1541106352796 | "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36"            |        8 |

```
`Information taken from Udacity Nano degree Programme`
### AWS Config File:
This file consists of all the configuration required to connect to aws and reshift cluster.

### Redshift_cluster.ipynb 
Notebook file to create Redshift cluster 

### SQL Scripts:
1. sql_quries: All the PostgreSQL statements for Copying, Creating, Dropping, Inserting, and Selection.

### Python Scripts:
1. database.py: The script will connect to the default database, then drop all the tables in Sparkify Database, and then create all the tables from scratch by executing `sql_quires` file.

2. Etl.py: The script used for running the following task using database.py:
    1. Load data from S3 to redshift staging tables `staginf_event` and `staging_songs` using `COPY` command from `S3` bucket.
    2. Transforms song and event data into Sparkify Star Schema (seen below)
    
## Execution of the project
1. Execute in `terminal:` `python etl.py`. This will extract, transform, and finally load the data in the database.

## ERD for sparkify
![alt text](Sparkify_STAR_ERD.png "Logo Sparkify ERD")

## ETL process for sparkify
![alt text](Sparkify%20ETL%20Process.png "ETL process")
