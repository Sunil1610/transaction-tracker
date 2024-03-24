import os.path
import base64
import json
import re
import time
import dbService as db
from transactions import get_timestamp
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import logging
import requests

from parsers.html_parser import extract_text_from_html

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def readEmails(extractor:str, limit:int):
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
                'credentials.json', SCOPES, redirect_uri='http://localhost:9000/')
            creds = flow.run_local_server(port=9000)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    if os.path.exists('./parsers/mail_parser_config.json') :
        with open('./parsers/mail_parser_config.json', 'r') as file:
            mail_parser_config = json.load(file)
            try:
                # Call the Gmail API
                service = build('gmail', 'v1', credentials=creds)
                page_token = None
                results = service.users().messages().list(userId='me', labelIds=['INBOX'], q =mail_parser_config[extractor]['query_string'], pageToken = page_token).execute()
                messages = results.get('messages', [])
                count = 0
                if not messages:
                    print('No new messages.')
                else:
                    for message in messages:
                        if(count > limit):
                            break
                        msg = service.users().messages().get(userId='me', id=message['id']).execute()
                        email_data = msg['payload']['headers']
                        for values in email_data:
                            name = values['name']
                            if name == 'From':
                                from_name = values['value']
                            if name == 'Subject':
                                subject = values['value']
                        for part in msg['payload']['parts']:
                            try:
                                data = part['body']['data']
                                byte_code = base64.urlsafe_b64decode(data)
                                text = extract_text_from_html(byte_code.decode("utf-8")).replace('\n', ' ')
                                pattern = re.compile(mail_parser_config[extractor]['regex'][2:-1], re.DOTALL)
                                match = pattern.search(text)
                                transaction = {}
                                if match:
                                    i = 1
                                    for val in mail_parser_config[extractor]['fields']:
                                        transaction[val] = match.group(i)
                                        i = i+1
                                source = ""
                                for val in transaction.keys() :
                                    for source_map in mail_parser_config[extractor]['source_mapping']:
                                        if(val in source_map) :
                                            if( source_map[val] == transaction[val]):
                                                source = source_map['Source']
                                transaction["Source"] = source
                                transaction["Type"] = mail_parser_config[extractor]['tran_type']
                                transaction["timestamp"] = get_timestamp(transaction['Date'], transaction['Time'])
                                count = count + 1
                                db.create_transaction(transaction, "transactions")
                                print (transaction)
                            except BaseException as error:
                                pass
                print(count)
            except Exception as error:
                print(f'An error occurred: {error}')
