"""
Functions to download file from google drive to local drive using google drive api
"""
from googleapiclient.discovery import build
from googleapiclient import errors, http
from googleapiclient.http import MediaIoBaseDownload
import io
import os
from os.path import join
from credentials import get_credential
from utils import get_download_path


def get_drive_service(creds):
    return build('drive', 'v3', credentials=creds, cache_discovery=False)

def call_file_info_api(service):
    try:
        response = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name, mimeType)").execute()
        return response
    except errors.HttpError as error:
        print("An error occurred: %s" % error)
        raise

def call_get_media_api(service, file_id):
    try:
        response = service.files().get_media(fileId=file_id)
        return response
    except errors.HttpError as error:
        print("An error occurred: %s" % error)
        raise

def call_export_api(service, file_id, extension_type, file_mime_type):
    try:
        response = service.files().export(fileId=file_id,
                                                 mimeType=extension_type[file_mime_type][0])
        return response
    except errors.HttpError as error:
        print("An error occurred: %s" % error)
        raise

def get_drive_file_names(creds):
    service = get_drive_service(creds)

    # Call the Drive v3 API
    response = call_file_info_api(service)
    items = response.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('==========Files==========:')
        for item in items:
            print(u'{0} ({1}, {2})'.format(
                item['name'], item['id'], item['mimeType']))
    return items


def download_file_from_drive():
    extension_type = {
        'application/vnd.google-apps.presentation': ['application/vnd.openxmlformats-officedocument.presentationml.presentation', 'ppt'],
        'application/vnd.google-apps.spreadsheet': ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'xls'],
        'application/vnd.google-apps.document': ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'docx']
    }
    mime_type_of_folder = 'application/vnd.google-apps.folder'

    creds = get_credential()
    service = get_drive_service(creds)
    items = get_drive_file_names(creds)
    for item in items:
        print('\nInitiating download of file: %s\n' % item['name'])
        file_name = item['name']
        file_id = item['id']
        file_mime_type = item['mimeType']

        if file_mime_type != mime_type_of_folder:
            if file_mime_type not in extension_type:
                request = call_get_media_api(service, file_id)
            else:
                request = call_export_api(service, file_id, extension_type, file_mime_type)

            download_path = get_download_path()
            fh = io.FileIO(join(download_path, file_name), 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                try:
                    status, done = downloader.next_chunk()
                    print("==========Download %d%%.==========" %
                          int(status.progress() * 100))
                except errors.HttpError as error:
                    print("An error occurred: %s" % error)


if __name__ == '__main__':
    download_file_from_drive()
