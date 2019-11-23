"""
Contains test cases for credentials.py
"""
import os
import pytest
from mock import patch
from google.oauth2.credentials import Credentials
from credentials import get_credential, load_creds_from_file, run_auth_server, save_creds, validate_token_and_secret_file_path


class TestCredentials(object):
    function_list = [get_credential, load_creds_from_file,
                     run_auth_server, save_creds, validate_token_and_secret_file_path]


    @pytest.mark.parametrize('function_name', function_list)
    def test_callable(self, function_name):
        assert callable(function_name)

    class TestLoadCredsFromFile(object):
        def test_return_type(self):
            token_file_path = '/google_drive_api/src/token.pickle'
            response = load_creds_from_file(token_file_path)
            assert isinstance(response, Credentials)

        def test_with_invalid_token(self):
            token_file_path = '/dummy/path/token.pickle'
            with pytest.raises(Exception):
                load_creds_from_file(token_file_path)

    class TestRunAuthServer(object):
        def test_with_invalid_path(self):
            secret_file_path = '/dummy/path/credentials.json'
            with pytest.raises(Exception):
                run_auth_server(secret_file_path)

    class TestSaveCreds(object):
        def test_return_type(self):
            token_file_path = '/google_drive_api/src/token.pickle'
            creds = load_creds_from_file(token_file_path)
            response = save_creds(token_file_path, creds)
            assert isinstance(response, bool)

        def test_with_invalid_token_path(self):
            token_file_path = '/google_drive_api/src/token.pickle'
            creds = load_creds_from_file(token_file_path)
            with pytest.raises(Exception):
                save_creds('/dummy/path/token.pickle', creds)

    class TestValidateTokenAndSecretFilePath(object):
        def test_with_valid_path(self):
            token_file_path = '/google_drive_api/src/token.pickle'
            secret_file_path = '/google_drive_api/src/credentials.json'
            res, message = validate_token_and_secret_file_path(
                secret_file_path, token_file_path)
            assert isinstance(res, bool)
            assert isinstance(message, str)
            assert res == True
            assert message == "Success"

        def test_with_invalid_path(self):
            token_file_path = '/dummy/path/token.pickle'
            secret_file_path = '/dummy/path/credentials.json'
            res, message = validate_token_and_secret_file_path(
                secret_file_path, token_file_path)
            assert isinstance(res, bool)
            assert isinstance(message, str)
            assert res == False
            assert message == 'Please Provide Valid Token and Secret Files'

    class TestGetCredential(object):

        def setup_method(self, test_method):
            token_file_path = '/google_drive_api/src/token.pickle'
            creds = load_creds_from_file(token_file_path)
            self.creds = creds

        def test_return_type(self):
            response = get_credential()
            assert isinstance(response, Credentials)


