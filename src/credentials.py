import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from utils import get_secret_file_path, get_token_file_path

secret_file_path = get_secret_file_path()
token_file_path = get_token_file_path()

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
    valid, message = validate_token_and_secret_file_path(
        secret_file_path, token_file_path)

    if not valid:
        print(message)
        return

    creds = load_creds_from_file(token_file_path)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = run_auth_server(secret_file_path)

        # Save the credentials for the next run
        save_creds(token_file_path, creds)

    return creds


def load_creds_from_file(token_file_path):
    """
    Get already saved credentials
    """
    with open(token_file_path, 'rb') as token:
        creds = pickle.load(token)
    return creds


def run_auth_server(secret_file_path):
    """
    Run local server for asking permission to access drive
    """
    flow = InstalledAppFlow.from_client_secrets_file(
        secret_file_path, SCOPES)
    creds = flow.run_local_server(port=2525)
    return creds


def save_creds(token_file_path, credential):
    """
    Save credentials to pickle file for future use
    """
    with open(token_file_path, 'wb') as token:
        pickle.dump(credential, token)


def validate_token_and_secret_file_path(token_file_path, secret_file_path):
    if os.path.exists(token_file_path) and os.path.exists(secret_file_path):
        return True, 'Success'
    return False, 'Please Provide Valid Token and Secret Files'
