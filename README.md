# Spotify ETL Data Pipeline

Python code reads from Spotify's API, extracts, transforms, and loads data into BigQuery/Google Sheets. Code is dockerized and ran every hour via GCP Cloud Run Jobs.

Data is batch streamed every hour, every day!!! 

Implements:
- containerization
- OOP / Modularity
- logging
- configuration
- data modeling/transformation
- job alerts via Slack

Code within this project integrates previous code build from my Strava ETL pipeline.
