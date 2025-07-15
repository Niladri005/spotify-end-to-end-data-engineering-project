# spotify-end-to-end-data-engineering-project
In this project, I will build an ETL(extract, Transform, Load) pipeline using Spotify API on AWS. The pipeline will retrieve data from the Spotify API, transform it to a desired format, and load it into an AWS data store.

# 🎧 Spotify Data Engineering ETL Pipeline using AWS

![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-orange?logo=amazon-aws&logoColor=white)
![S3](https://img.shields.io/badge/AWS-S3-blue?logo=amazon-aws)
![Python](https://img.shields.io/badge/Python-3.8+-green?logo=python)
![Status](https://img.shields.io/badge/Project-Completed-brightgreen)



---

## 📌 Overview

This project demonstrates a **complete data engineering ETL pipeline** that extracts data from the **Spotify API**, processes it with **AWS Lambda**, stores it in **Amazon S3**, and queries it using **AWS Athena** through the **Glue Data Catalog**.

---
## 📷 Architecture
![Architecture Diagram]()

---
## 🧠 Key Features
🎯 Integration with Spotify API using spotipy

⚙️ Serverless ETL pipeline using AWS Lambda

🔄 Hourly scheduled data ingestion

🧹 On-the-fly data transformation

📂 Organized raw and processed data in S3

🧭 Schema detection via AWS Glue Crawler

🧠 SQL analysis through Amazon Athena

---
## 🛠️ Services & Tools Used

| Service         | Description                                                                 |
|-----------------|-----------------------------------------------------------------------------|
| **Spotify API** | Provides real-time data about artists, albums, and tracks                  |
| **AWS Lambda**  | Executes extract and transform Python code in a serverless environment     |
| **Lambda Layer**| Includes external library `spotipy` needed in Lambda                       |
| **Amazon S3**   | Stores both raw and transformed JSON data                                  |
| **IAM Role**    | Grants Lambda access to S3                                                 |
| **CloudWatch**  | Monitors and logs function execution                                       |
| **AWS Glue**    | Crawls transformed data and catalogs schema                                |
| **Amazon Athena**| Runs SQL queries directly over S3 data                                     |

---
## 💻 Python Packages Used

Install the required libraries locally:

bash
pip install pandas
pip install numpy
pip install spotipy
---
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import boto3
import pandas as pd
import numpy as np

---
## 🔧 Setup & Deployment

### 🔹 1. Create S3 Bucket

Organize your S3 buckets like this:
```
s3://spotify-etl-project-niladri05/
├── raw_data/
│ ├── already_processed/
│ └── to_process/
└── transformed_data/
├── artist/
├── songs/
└── album/
```
---

### 🔹 2. Extract Lambda Function

- Add environment variables:
  - `SPOTIPY_CLIENT_ID`
  - `SPOTIPY_CLIENT_SECRET`
- Uploaded my Lambda function code
- Attached IAM roles:
  - `AmazonS3FullAccess`
  - `AWSLambdaRole`

---

### 🔹 3. Create Lambda Layer

Since AWS Lambda does not support direct pip installations, create a Lambda Layer:

```bash
pip install spotipy -t python/
zip -r spotipy_layer.zip python/
Upload the ZIP file as a new Lambda Layer
```
Attach the layer to your Lambda function

### 🔹 4. Set Lambda Trigger
Use Amazon CloudWatch (EventBridge) to schedule the extract Lambda every 1 hour

### 🔹 5. Transformation Lambda Function
Reads .json files from the to_process/ folder

Transforms and cleans the data

Writes processed files to the transformed_data/ folder

Moves raw files from to_process/ to /already_processed/

### 🔹 6. Glue Crawler & Data Catalog
Create a Glue Crawler to scan transformed_data/

This will create the following tables in the Glue Data Catalog:
artist
album
songs (or track)

### 🔹 7. Query with Athena
Run SQL queries on the data like this:

SELECT * FROM artists LIMIT 10;





## 🙋‍♂️ Author

**Niladri Goswami**  
🧑‍💻 Software Engineer | Data Enthusiast  

- 🔗 [LinkedIn](https://www.linkedin.com/in/)
- 🔗 [GitHub](https://github.com/)
