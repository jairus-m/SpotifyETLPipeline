import pandas as pd
import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials
from processDataset import processData
import json

def uploadData(df: pd.DataFrame, spreadsheet_key: str, wks_name: str, gs_credentals_json: json):
    """
    This function uploads the dataframe as a csv to google sheets.
    Args:
        pandas dataframe : activitiy data
    Returns:
        None
    """

    scope = ['https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(gs_credentals_json, scope)
    gc = gspread.authorize(credentials)


    spreadsheet_key = '1cN18XshR_r-xvRGJiW0qU8dKP6amzsm8amPHXgLmRyg'
    wks_name = 'StravaData'
    # upload csv to google sheets
    d2g.upload(df, spreadsheet_key, wks_name, credentials=credentials, row_names=True)

    return None