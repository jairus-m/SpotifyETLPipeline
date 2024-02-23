# Spotify ETL Data Pipeline

Python code reads from Spotify's API, extracts, transforms, and loads data into BigQuery. Code is containerized with Docker and ran every hour via GCP Cloud Run Jobs.

Data is batch processed every hour, every day!!! 

Implements:
- ETL design
- containerization
- OOP / Modularity
- logging
- configuration
- data modeling/transformation
- job alerts via Slack

Code within this project integrates previous code build from my Strava ETL pipeline.
