import os.path
import csv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive"]

file_name = "test.csv"

class GoogleDriveSync:
    def __init__(self):
        self.cred = self.__authentication()

    def __authentication(self):
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        return creds

    def update_file(self, local_file_name, drive_file_name):
        try:
            service = build("drive", "v3", credentials=self.cred)

            # get file id
            query_params = {
                'q': f"name='{drive_file_name}'",
                'pageSize': 1,
                'fields': "files(id, name)"
            }
            result = service.files().list(**query_params).execute()
            file = result.get('files', [])
            if not file:
                # create the file
                file_metadata = {
                    'name': drive_file_name,
                    'mimeType': 'text/csv'
                }
                service.files().create(body=file_metadata).execute()
                print("File created")
            file_id = file[0].get('id')

            # download the drive file
            drive_data = service.files().export_media(fileId=file_id, mimeType="text/csv").execute().decode('utf-8')
            # sort the data by first column
            temp = drive_data.splitlines()
            temp.sort(key=lambda x: x.split(",")[0], reverse=True)
            csv_list = []
            for line in csv.DictReader(temp):
                csv_list.append(line)
            old_websites = set(data["Link"] for data in csv_list)
            old_dict = {data["Link"]: data for data in csv_list}
            print("Download Complete")

            # Load local file
            content = []
            with open(local_file_name, "r") as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames
                for row in reader:
                    content.append(row)
            content_dict = {data["Link"]: data for data in content}
            current_websites = set(content_dict.keys())

            # compare the two versions and update the local file
            all_websites = current_websites.union(old_websites)
            print("difference: ", current_websites.difference(old_websites))
            data = []
            for website in all_websites:
                if website in old_websites:
                    data.append(old_dict[website])
                else:
                    data.append(content_dict[website])
            with open(local_file_name, "w") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)

            # upload the updated file
            media = MediaFileUpload(local_file_name, mimetype="text/csv", resumable=True)
            
            service.files().update(fileId=file_id, media_body=media).execute()
            print("File updated")

        except HttpError as error:
            print(f"An error occurred: {error}")