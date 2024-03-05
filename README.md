# Spotify ETL Data Pipeline

![SpotifyETL](https://github.com/jairus-m/SpotifyETLPipeline/assets/114552516/ee914bc7-5e4a-4869-97f8-d4cd81693033)

Python code reads from Spotify's API, extracts, transforms, and loads data into BigQuery. Code is containerized with Docker and ran every hour via GCP Cloud Run Jobs.

Data is batch processed every hour, every day!!! 

Implements:
- containerization
- OOP / Modularity
- logging
- configuration
- data modeling/transformation
- job alerts via Slack

Code within this project integrates previous code build from my Strava ETL pipeline.
