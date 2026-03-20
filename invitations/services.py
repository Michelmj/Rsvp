import os
import gspread
from django.conf import settings
from oauth2client.service_account import ServiceAccountCredentials


def append_to_google_sheet(name, spouse, email, number, response):
    # Setup credentials
    scope = ["https://spreadsheets.google.com"]
    
    creds_path = os.path.join(settings.BASE_DIR, 'credentials.json')
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)

    # Open the sheet by its name
    sheet = client.open("SephoMario").worksheet("rsvp")
    
    # Append the row
    sheet.append_row([name, email, number, response])