from __future__ import print_function

import os.path
import spacy
import base64
import codecs
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Load Spacy language model
nlp = spacy.load('en_core_web_sm')
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
# Define label mappings
LABELS = {'health': 'Health', 'job': 'Job', 'education': 'Education',
          'ad': 'Advertisement', 'general': 'General'}


def has_education_content(doc):
    """This function checks for Educational content in the provided text

    Args:
        doc (Doc): Spacy Doc Object

    Returns:
        Boolean Value: returns True or False
    """
    # Check for education-related keywords
    education_keywords = ['lesson', 'tutor', 'blog', 'article', 'lecture', 'diagram',
                          'literature', 'art', 'technology', 'science', 'history', 'religion', 'blog']
    for token in doc:
        if token.lemma_.lower() in education_keywords:
            return True

    return False


def has_medical_content(doc):
    """This function checks for Medical content in the provided text

    Args:
        doc (Doc): Spacy Doc Object

    Returns:
        Boolean Value: returns True or False
    """
    # Check for medical-related entities
    for entity in doc.ents:
        if entity.label_ == 'DRUG' or entity.label_ == 'DISEASE':
            return True

    # Check for medical-related keywords
    medical_keywords = ['medical', 'health', 'blood', 'dr', 'report', 'tests',
                        'medicine', 'hospital', 'doctor', 'patient']
    for token in doc:
        if token.lemma_.lower() in medical_keywords:
            return True

    return False


def has_job_application_content(doc):
    """This function checks for Career related content in the provided text

    Args:
        doc (Doc): Spacy Doc Object

    Returns:
        Boolean Value: returns True or False
    """
    # Check for job application-related keywords
    job_keywords = ['resume', 'CV', 'curriculum vitae', 'candidate', 'interview', 'profile', 'Relevant Exp',
                    'cover letter', 'application', 'job', 'JD', 'job description', 'notice period']
    for token in doc:
        if token.lemma_.lower() in job_keywords:
            return True

    return False


def has_shopping_content(doc):
    """This function checks for Shopping related content in the provided text

    Args:
        doc (Doc): Spacy Doc Object

    Returns:
        Boolean Value: returns True or False
    """
    # Check for job application-related keywords
    ad_keywords = ['shopping', 'buy', 'purchase', 'deal',
                    'discount', 'sale', 'offer', 'promo', 'ad', 'advertisement']
    for token in doc:
        if token.lemma_.lower() in ad_keywords:
            return True

    return False


def analyze_message_text(text):
    """_summary_

    Args:
        text : Message Body or Snippet can be passed for analytics

    Returns:
        labels: Specific Labels based on Message content
    """
    doc = nlp(text)
    # Check for keywords indicating different categories
    if has_education_content(doc):
        return 'education'
    elif has_medical_content(doc):
        return 'health'
    elif has_job_application_content(doc):
        return 'job'
    elif has_shopping_content(doc):
        return 'ad'
    else:
        return 'general'


def modify_message_label(service, message_id, label):
    """_summary_

    Args:
        service : Google Resource Object for interacting with related functions
        message_id : Id of the message/mail
        label : Label of the message of mail, which is to be modified
    """
    # Modify the label of a specific message
    message = service.users().messages().get(userId='me', id=message_id).execute()

    # Get the current labels
    current_labels = message['labelIds']

    # Remove any existing labels
    current_labels.remove('INBOX')

    # Add the new label
    current_labels.append(label)

    # Update the message with the new label
    message['labelIds'] = current_labels
    service.users().messages().update(
        userId='me', id=message_id, body=message).execute()


def main():
    getMessages()


def getMessages():
    """This function fetches messages or mails from Gmail Account and performs analytics
    """
    creds = connect_Google_API()

    try:
        service = build('gmail', 'v1', credentials=creds)
        # Call the Gmail API

        messagesResult = service.users().messages().list(userId='me').execute()
        messages = messagesResult.get('messages', [])
        # Limit the number of messages to process
        messages = messages[:20]

        if not messages:
            print('No messages found.')
            return
        print('Messages:')
        for message in messages:
            message_id = message['id']
            # Get the message it self
            m = service.users().messages().get(
                userId='me', id=message['id']).execute()
            # m['snippet'] is the message it self
            snippet = m['snippet']
            body = ''
            if 'parts' in m['payload']:
                # If the message has multiple parts, concatenate them
                for part in m['payload']['parts']:
                    if 'body' in part:
                        body += part['body'].get('data', '')
            elif 'body' in m['payload']:
                body = m['payload']['body'].get('data', '')

            body = base64.urlsafe_b64decode(body).decode('utf-8')
            label = analyze_message_text(text=snippet)
            print(f"{label} : \n{snippet}")
            # modify_message_label(service=service, message_id=message_id, label=LABELS[label])

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


def connect_Google_API():
    """    
    Connects to the Google API by obtaining and validating user credentials.

    Returns:
        creds (google.auth.credentials.Credentials): Valid user credentials for accessing the Google API.
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
    return creds


if __name__ == '__main__':
    main()
