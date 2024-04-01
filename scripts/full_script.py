import os
from turtle import down

from urllib import response
import google.oauth2.credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
import requests
import io

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

def list_files_in_drive(creds,service,folder_id):
    query=f"'{folder_id}' in parents and trashed=false"

    results = service.files().list(
        pageSize=10, q=query,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
            
        return items





def upload_file(service):
    url='https://www.googleapis.com/upload/drive/v3/files?uploadType=media'
    file_path='new_dummy.txt'
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

    

def upload_files_dir(dir_path,service,parents):
    for filename in os.listdir(dir_path):
        file_path=os.path.join(dir_path,filename)
        if os.path.isfile(file_path):
            file_metadata={
                'name':filename,
                'mimetype':'text/plain',
                'parents':[parents]
            }
            upload_file_multipart(service,file_metadata)
        else:
            raise Exception("The file ",file_path,"doesnt exist")

def upload_file_multipart(service,metadata):
    print("im here")
    media=MediaFileUpload(metadata['name'], mimetype=metadata['mimetype'])
    file_metadata={
        'name':metadata['name'],
        'parents':metadata.get('parents',[])
    }
    print(file_metadata['parents'])
    file=service.files().create(body=file_metadata,media_body=media).execute()
    if file:
        print("File succesfully written")
    else:
        raise Exception("File backup didnt work")

def download_files(creds,service,folder):
    items=list_files_in_drive(creds,service,folder)
    for item in items:
        file_name=item['name']
        req=service.files().get_media(fileId=item['id'])
        file = io.BytesIO()
        downloader=MediaIoBaseDownload(file,req)
        done=False
        while not done:
            status,done=downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}.")
        with open(file_name,'wb') as f:
            f.write(file.getvalue())
        print(f"File {file_name} downloaded succesfully")



if __name__ == '__main__':
    creds,service=get_access()
    dir_in_drive='1ErvoMWmEUS3kp3Ltswr_o0dDLK8q3ubp'
    # upload_files_dir("our_folder",service,dir_in_drive)
    # list_files_in_drive(creds,service,dir_in_drive)

    download_files(creds,service,dir_in_drive)
