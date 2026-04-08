# Spotify Serverless ETL Pipeline on AWS

## Overview
This project implements a serverless ETL pipeline using AWS Lambda and Amazon S3 to extract artist data from the Spotify API, store raw JSON data, transform it into structured CSV format, and load it into S3 for analytics.

## Architecture
Spotify API → AWS Lambda → S3 (raw) → Transform → S3 (processed)

## Technologies Used
- Python
- AWS Lambda
- Amazon S3
- IAM
- Spotify Web API

## ETL Workflow
### Extract
- Authenticate with Spotify API
- Fetch artist data

### Raw Load
- Save JSON to S3 raw layer

### Transform
- Clean and structure artist metadata

### Processed Load
- Save transformed CSV to S3 processed layer

## Security
- Used environment variables for credentials
- IAM role for secure S3 access

## Key Learnings
- API authentication
- Serverless pipelines
- S3 data lake structure
- IAM debugging
## Future Improvements
- Add scheduled execution using EventBridge
- Expand to multiple artists
- Add analysis and visualization layer
