import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def append_to_google_sheet(name, spouse, email, number, response):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    # Read credentials from environment variable
    creds_json = os.environ.get('GOOGLE_CREDENTIALS')
    creds_dict = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    # Open the sheet
    sheet = client.open("SephoMario").worksheet("RSVP")

    # Append the row
    sheet.append_row([name, spouse, email, number, response])