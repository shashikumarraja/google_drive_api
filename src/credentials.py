import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SECRET_FILE_PATH = os.environ['secret_file'] if 'secret_file' in os.environ else 'credentials.json'
TOKEN_FILE_PATH = os.environ['token_file'] if 'token_file' in os.environ else 'token.pickle'

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']


def get_credential():
    """
    Returns the credentials to access the google drive api
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_FILE_PATH):
        with open(TOKEN_FILE_PATH, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                SECRET_FILE_PATH, SCOPES)
            creds = flow.run_local_server(port=2525)

        # Save the credentials for the next run
        with open(TOKEN_FILE_PATH, 'wb') as token:
            pickle.dump(creds, token)
    return creds