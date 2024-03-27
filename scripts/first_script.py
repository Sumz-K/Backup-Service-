import os
from urllib import response
import google.oauth2.credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import requests

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file']
API_KEY = ''

# OAuth 2.0 credentials
CLIENT_ID = ''
CLIENT_SECRET = ''

def authenticate():
    flow = InstalledAppFlow.from_client_config({
        'installed': {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uris': ['urn:ietf:wg:oauth:2.0:oob'],
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://accounts.google.com/o/oauth2/token'
        }
    }, SCOPES)
    creds = flow.run_local_server(port=0)
    return creds




def get_access():
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds, developerKey=API_KEY)
    return creds,service

def list_files_in_drive(creds,service):
    
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))





def upload_file(service):
    url='https://www.googleapis.com/upload/drive/v3/files?uploadType=media'
    file_path='dummy.txt'
    access_token = service._http.credentials.token
    with open(file_path, "rb") as file:
        file_data = file.read()
    headers={
        "Authorization": "Bearer {}".format(access_token),
        "Content-Type":"text/plain",
        "Content-Length":str(len(file_data))
    }
    response=requests.post(url,data=file_data,headers=headers)
    print(response.text,response.status_code)

    


def upload_file_multipart(service,metadata):
    media=MediaFileUpload(metadata['name'], mimetype=metadata['mimetype'])
    file_metadata={
        'name':metadata['name'],
        'parents':metadata.get('parents',[])
    }
    file=service.files().create(body=file_metadata,media_body=media).execute()
    



if __name__ == '__main__':
    creds,service=get_access()
    file_metadata={"name":"dummy.txt","parents":['1ErvoMWmEUS3kp3Ltswr_o0dDLK8q3ubp'],'mimetype':'text/plain'}
    
    upload_file_multipart(service,file_metadata)


    


