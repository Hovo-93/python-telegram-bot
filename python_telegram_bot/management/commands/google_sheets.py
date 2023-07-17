import os
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
from python_telegram_bot.models import Notification
import gspread

load_dotenv(dotenv_path='.env')
# todo
# Define the dynamic range parameters
start_row = 2
end_row = 5
start_column = 'A'
end_column = 'E'
dynamic_range = f"{start_column}{start_row}:{end_column}{end_row}"


def save_parsing_data(telegram_id, text, date, time, answer_time):
    notification_user, created = Notification.objects.get_or_create(
        telegram_id=telegram_id,
        defaults={
            'text': text,
            'date': date,
            'time': time,
            'answer_time': answer_time,
        }
    )
    print(f"User is Created:f'{notification_user}")

    if not created:
        # If the user is not newly created (created is False), we update the user's information (text, date,  time,answer_time) and save the changes.
        notification_user.text = text
        notification_user.data = date
        notification_user.time = time
        notification_user.answer_time = answer_time
        notification_user.save()
        print("User info updated:", notification_user)


class Command(BaseCommand):
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    SPREADSHEETS_ID = os.getenv('SPREADSHEETS_ID')
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    def handle(self, *args, **options):
        credentials = None
        if os.path.exists("token.json"):
            credentials = Credentials.from_authorized_user_file("token.json", self.SCOPES)
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'python_telegram_bot/credentials.json', self.SCOPES)
                credentials = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(credentials.to_json())
        try:
            service = build('sheets', 'v4', credentials=credentials)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=self.SPREADSHEETS_ID,
                                        range=dynamic_range).execute()
            values = result.get('values', [])

            client = gspread.authorize(credentials)

            data = self.get_column_values(client)
            print(data)
            for row in data:
                telegram_id, text, date, time, answer_time = row
                # google_sheets date format change to django date format
                date = datetime.strptime(date, '%d.%m.%Y').date()
                answer_time = timedelta(hours=int(answer_time))

                save_parsing_data(telegram_id=telegram_id,
                                  text=text,
                                  time=time,
                                  date=date,
                                  answer_time=answer_time)
            print("Data saved to the database successfully.")


        except HttpError as err:
            print(err)

    def get_column_values(self, client):
        sheet = client.open_by_key(self.SPREADSHEETS_ID)
        worksheet = sheet.get_worksheet(0)
        range_str = f"{start_column}:{end_column}"
        values = worksheet.get(range_str)
        data = values[1:]
        return data

# 1. parse/save notifications from sheet

# 2. crons: every minute: run sender and run parser

# 3. sender: db::whereNull(message_id)->where(notification_date,today())->time()
# 4.
