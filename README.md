# Spotify Serverless ETL Pipeline on AWS
AWS Lambda + S3 + Spotify API ETL pipeline

## Overview
This project implements a serverless ETL pipeline using AWS Lambda and Amazon S3 to extract artist data from the Spotify API, store raw JSON data, transform it into structured format, and load the processed data into S3 for analytics.

## Architecture
Spotify API → AWS Lambda → S3 (raw) → Transform → S3 (processed)

## Technologies Used
- Python
- AWS Lambda
- Amazon S3
- IAM
- Spotify Web API

## ETL Workflow

### 1. Extract
- Authenticate with Spotify API using Client Credentials Flow
- Retrieve artist metadata

### 2. Load (Raw Layer)
- Store full API response in S3 as JSON:
  - `raw/spotify_raw.json`

### 3. Transform
- Extract relevant fields:
  - artist_name
  - artist_id
  - popularity
  - followers
  - genres
  - spotify_url

### 4. Load (Processed Layer)
- Save structured data to S3 as CSV:
  - `processed/spotify_processed.csv`

## Security
- Used environment variables for API credentials
- Managed permissions via IAM roles
- Resolved S3 access issues with Lambda execution role policies

## Key Learnings
- API integration with authentication
- Serverless execution with AWS Lambda
- Raw vs processed data layer design
- IAM debugging and permissions handling
- ETL pipeline design principles

## Future Improvements
- Add scheduled execution using EventBridge
- Expand to multiple artists
- Add analysis and visualization layer
