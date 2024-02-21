"""Main entry point for Spotify ETL job"""

import argparse
import logging
import logging.config
import time
import datetime
import yaml
import logging
from utils import GoogleSheetsConnector, SlackNotifications, SpotifyConnector

def parse_config():
    """Parse YAML config file from CLI arg input"""
    parser = argparse.ArgumentParser(description='Run the Spotify ELT Job.')
    parser.add_argument('config', help='A configuration file in YAML format.')
    args = parser.parse_args()
    config = yaml.safe_load(open(args.config, encoding='utf-8'))
    return config

def initialize_logging(config):
    """
    Initialize logging
    
    :param config: yaml config that is read in
    """
    log_config = config['logging']
    logging.config.dictConfig(log_config)

def initialize_slack(config):
    """
    Initialize SlackNotifications

    :param config: yaml config that is read in
    """
    channel = config['slack']['channel']
    token = config['slack']['token']
    slack = SlackNotifications(token, channel)
    return slack

def initialize_connectors(config):
    """
    Initialize the Strava and Bigquery connectors.

    :param config: yaml config that is read in
    """
    gsc = GoogleSheetsConnector.GoogleSheetData(
        config['google_sheets']['scope'],
        config['google_sheets']['spreadsheet_url'],
        config['google_sheets']['json_credentials_path']
    )
    sc = SpotifyConnector.SpotifyData(
        config['spotify']['client_id'],
        config['spotify']['client_secret']
    )
    
    return gsc, sc

def main():
    """Entry point for Strava ETL job"""
    try:
        start_time = time.time()
        
        config = parse_config()
        initialize_logging(config)
        slack = initialize_slack(config)
        gsc, sc = initialize_connectors(config)

        logger = logging.getLogger(__name__)
        logger.info('Starting ETL job.')

        # get old data
        df_old = gsc.get_sheets_data()
        
        # get recent data
        songs = sc.get_songs()
        df_new = sc.create_song_data(songs)

        # upload data
        gsc.upload_new_data(df_new, df_old)

        logger.info('ETL job complete.')

        duration = time.time() - start_time

        slack.timing_message(job='Spotify_ETL', duration=duration)
        slack.send_custom_message('Job succeeded!')
    except Exception as e:
        slack.send_custom_message(f'Date: {datetime.datetime.now()}\nSpotifyETL job failed. Please check logs.')
        slack.send_custom_message(f'Exception: {e}')