"""
Contains utility functions to be used across project
"""
import errno
import os
from os import path
from os.path import join, dirname

def create_download_path(folder_path):
    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    return folder_path

def get_download_path():
    DOWNLOAD_PATH = os.environ['download_path'] if 'download_path' in os.environ else ''
    default_path = join(dirname(__file__), 'downloads')
    download_path = DOWNLOAD_PATH if os.path.exists(DOWNLOAD_PATH) else create_download_path(default_path)
    return download_path

def get_secret_file_path():
    SECRET_FILE_PATH = os.environ['secret_path'] if 'secret_path' in os.environ else ''
    default_path = join(dirname(__file__), 'credentials.json')
    path = SECRET_FILE_PATH if os.path.exists(SECRET_FILE_PATH) else default_path
    return path

def get_token_file_path():
    TOKEN_FILE_PATH = os.environ['token_path'] if 'token_path' in os.environ else ''
    default_path = join(dirname(__file__), 'token.pickle')
    path = TOKEN_FILE_PATH if os.path.exists(TOKEN_FILE_PATH) else default_path
    return path
