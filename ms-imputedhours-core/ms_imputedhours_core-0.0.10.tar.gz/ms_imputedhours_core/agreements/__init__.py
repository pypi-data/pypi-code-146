import os
import base64
import json
from datetime import datetime
from gc_google_services_api.gsheet import GSheet

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
]
RANGE_NAME = os.getenv('GOOGLE_SHEET_AGREEMENT_RANGE', 'A2:B8000')
CREDENTIALS_BASE64 = os.getenv('GOOGLE_SHEET_CREDENTIALS', '')
SHEET_NAMES_TO_IGNORE = ['Summary']

try:
    CREDENTIALS_CONTENT = json.loads(base64.b64decode(CREDENTIALS_BASE64))
except json.JSONDecodeError:
    CREDENTIALS_CONTENT = ''


class Agreements(object):
    def __init__(self, spreadsheet_id) -> None:
        self.spreadsheet_id = spreadsheet_id
        self.service = GSheet(CREDENTIALS_CONTENT, SCOPES)

    def get_hours_by_month(self, month, year, sheet_name):
        try:
            values = self.service.read_gsheet(sheet_name, self.spreadsheet_id, RANGE_NAME)
        except Exception as e:
            print('[ERROR] - get_hours_by_month: ', e)
            values = {'values': []}

        day_hours_data = {
            'totalHours': 0.0,
            'days': {}
        }
        for day_data in values['values']:
            day_obj = datetime.strptime(day_data[0], '%d/%m/%Y')
    
            if day_obj.month == month and day_obj.year == year:
                day_hours = '{}'.format(day_data[1]).replace(',', '.')
                day_hours_data['totalHours'] += float(day_hours)
                day_hours_data['days'][day_obj.day] = day_hours

        return day_hours_data

    def get_hours_by_range(self, from_date, to_date, sheet_name):
        try:
            values = self.service.read_gsheet(sheet_name, self.spreadsheet_id, RANGE_NAME)
        except Exception as e:
            print('[ERROR] - get_hours_by_range: ', e)
            values = {'values': []}

        day_hours_data = {
            'totalHours': 0.0,
            'days': {}
        }
        
        for day_data in values['values']:
            day_obj = datetime.strptime(day_data[0], '%d/%m/%Y')
            is_date_after_from_date = (day_obj.month, day_obj.year) >= (from_date.month, from_date.year)
            is_date_before_to_date = (day_obj.month, day_obj.year) <= (to_date.month, to_date.year)

            if is_date_after_from_date and is_date_before_to_date:
                is_day_after_from_date = (day_obj.day, day_obj.month) >= (from_date.day, from_date.month)
                is_dat_before_to_date = (day_obj.day, day_obj.month) <= (to_date.day, to_date.month)

                if is_day_after_from_date and is_dat_before_to_date:
                    day_key = '{}-{}'.format(day_obj.day,day_obj.month)
                    day_hours = '{}'.format(day_data[1]).replace(',', '.')
                    day_hours_data['totalHours'] += float(day_hours)
                    day_hours_data['days'][day_key] = day_hours

        return day_hours_data

    def get_all_office_names(self):
        try:
            values = self.service.get_sheetnames(self.spreadsheet_id)
        except Exception as e:
            print('[ERROR] - get_all_agreements: ', e)
            values = {}
        
        sheet_names = []
        for sheet in values.get('sheets', []):
            sheet_name = sheet['properties']['title']
            if sheet_name not in SHEET_NAMES_TO_IGNORE:
                sheet_names.append(sheet_name)

        return sheet_names
