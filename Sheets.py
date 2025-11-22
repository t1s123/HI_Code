import gspread
from google.oauth2.service_account import Credentials

class Sheets:
    def __init__(self,spreadsheet):
        scope = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

        creds = Credentials.from_service_account_file("service_account.json", scopes=scope)

        client = gspread.authorize(creds)

        self.sheet = client.open_by_url(spreadsheet)

    def get_sheet(self,spreadsheet,account):
        return self.sheet
    
    def get_sheet_by_name(self,name):
        return self.sheet.worksheet(name)