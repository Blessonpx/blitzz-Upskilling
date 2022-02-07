### 
### This is in code is in Particular to extacting Job Details from Linked In - Job Alerts 
### Lets you download the CSV file for all links thathave messaged you about vacacancies in Particular companies 
###

### Keep in Mind , the Underlying assumption is that you have already enabled Gmail for Exterernal API Calls for your project ,
### And have a basic Knowledge of WHat Google APIs do
### Also that you ahve downloaded the credentials for OAuth2 Authorization and saved as tokenn.json in the source run location
### for More info on Creating the above steps , refer the following Video
### https://www.youtube.com/watch?v=vgk7Yio-GQw    
### FYI , the Calls may exceed your Free API Calls Limit Within your account if using a personal account


import base64
import email
import os.path
import csv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re


###
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

## Create Service to be passed for further operations

def get_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        return service

    
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


## Create the base service
service=get_service()
## Call the Service Searching for Ids where Sender was from:jobalerts-noreply@linkedin.com
search_id=service.users().messages().list(userId='me',q='from:jobalerts-noreply@linkedin.com').execute()
# Collate messages  
email_id_list=search_id['messages']
id_list=[]
## Collect Ids for each Individual Email
for x in email_id_list:
    #print(x['id'])
    id_list.append(x['id'])
       
## Print to have a look (Optional)
print(id_list)
## List for accumulation of HTTP Links within the email
link_list=[]
for ids in id_list:
    message_list=service.users().messages().get(userId='me',id=ids,format='raw').execute()
    ## Base line Conversion for Basic messages 
    msg_raw=base64.urlsafe_b64decode(message_list['raw'].encode('ASCII'))
    msg_str=email.message_from_bytes(msg_raw)
    part1,part2=msg_str.get_payload()
    # Regex for Selecting The Particular lines that have the Company Link for Apply-ing for the Job 
    l=re.findall(r'(View job: https?://[^\s]+)', str(part1))
    for x in l:
        link_list.append(x)
print(link_list)
