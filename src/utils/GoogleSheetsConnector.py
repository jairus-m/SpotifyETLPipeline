"""This is the connector for the Google Sheets API"""

import logging
import pandas as pd 
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheetData():
    """
    Class object to interact with Google Sheets API
    
    Attributes:
        scope: scope of Google API
        credentials: oauth2client.service_account ServiceAccountCredentials
        gc: google credentials object
        spreadsheet_url: url to spreadsheet
        spreadsheet: spreadsheet object from gc
        worksheet: worksheet object

    Methods:
        get_sheets_data: downloads existing data from Google Sheets
        upload_new_data: uploads new data to Google Sheets
    """
    def __init__(self, scope: list, json_credentials_path: str, spreadsheet_url: str):
        self.scope = scope
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(json_credentials_path, self.scope)
        self.gc = gspread.authorize(self.credentials)
        self.spreadsheet_url = spreadsheet_url
        self.spreadsheet = self.gc.open_by_url(self.spreadsheet_url)
        self.worksheet = self.spreadsheet.get_worksheet(0)
        self._logger = logging.getLogger(__name__)
    
    def get_sheets_data(self) -> pd.DataFrame:
        """
        Downloads existing data from Google Sheets
        :return pd.DataFrame:
        """
        existing_data = self.worksheet.get_all_values()
        return pd.DataFrame(existing_data[1:], columns=existing_data[0])

    def upload_new_data(self, df_new: pd.DataFrame, df_old: pd.DataFrame) -> int:
        """
        Uploads new data to specified Google Sheets

        :param df_new: new data extracted from Spotify API
        :param df_old: old data extracted from existing Google Sheets API
        :return num_new_items: returns the nuber of new items added
        """
        # make sure the time col are datetime64
        df_new['time'] = df_new['time'].astype('datetime64[ns]')
        df_old['time'] = df_old['time'].astype('datetime64[ns]')
        try:
            latest_time = df_old['time'].astype('datetime64[ns]').sort_values(ascending=False)[0]
            newest_time = df_new['time'].sort_values(ascending=False)[0]

            if latest_time < newest_time:
                df_new = df_new.loc[df_new['time'] > latest_time]
                df = pd.concat([df_old, df_new]).sort_values(by='time', ascending=False)

                if len(df) > len(df_old):
                    # timestamp dtype is not JSON serializeable so convert back to str
                    df['time'] = df['time'].astype('str')

                    self.worksheet.update([df.columns.values.tolist()] + df.values.tolist())
                    self._logger.info(f'New data added: {len(df_new)} items.')
                    return len(df_new)
                else:
                    return 0
            else:
                self._logger.info('No new data to upload.')
                return 0

        except Exception as e:
            self._logger.info(f'Error in upload_new_data(): {e}')

        
        