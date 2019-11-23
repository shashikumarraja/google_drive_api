import os
import pytest
from mock import patch
import utils
from utils import get_download_path, get_secret_file_path, get_token_file_path, create_download_path

class TestUtils(object):
    function_list = [(get_download_path, str), (get_secret_file_path, str), (get_token_file_path, str)]

    @pytest.mark.parametrize('function_name, return_type', function_list)
    def test_callable_and_return_type(self, function_name, return_type):
        response = function_name()
        assert callable(function_name)
        assert isinstance(response, return_type)

    class TestDownloadPath(object):
        def test_with_valid_environ_path(self, monkeypatch):
            valid_path = os.getcwd()
            envs = {
                'download_path': valid_path
            }
            monkeypatch.setattr(os, 'environ', envs)
            path = get_download_path()
            assert path == valid_path

        def test_with_invalid_environ_path(self, monkeypatch):
            invalid_path = ''
            envs = {
                'download_path': invalid_path
            }
            monkeypatch.setattr(os, 'environ', envs)
            path = get_download_path()
            assert path == '/google_drive_api/src/downloads'

        def test_with_default_path(self):
            path = get_download_path()
            assert path == '/google_drive_api/src/downloads'

        @patch('utils.create_download_path')
        def test_oserror_while_path_creation(self, mocked_create_download_path):
            mocked_create_download_path.side_effect = OSError
            with pytest.raises(OSError):
                get_download_path()

        @patch('utils.create_download_path')
        def test_create_download_path_is_called(self, mocked_create_download_path):
            mocked_create_download_path.return_value = '/google_drive_api/src/downloads'
            get_download_path()
            mocked_create_download_path.assert_called_once_with('/google_drive_api/src/downloads')

    class TestSecretFilePath(object):

        def test_with_valid_environ_path(self, monkeypatch):
            valid_path = os.getcwd()
            envs = {
                'secret_path': valid_path
            }
            monkeypatch.setattr(os, 'environ', envs)
            path = get_secret_file_path()
            assert path == valid_path

        def test_with_invalid_environ_path(self, monkeypatch):
            invalid_path = ''
            envs = {
                'secret_path': invalid_path
            }
            monkeypatch.setattr(os, 'environ', envs)
            path = get_secret_file_path()
            assert path == '/google_drive_api/src/credentials.json'

        def test_with_default_path(self):
            path = get_secret_file_path()
            assert path == '/google_drive_api/src/credentials.json'

    class TestTokenFilePath(object):

        def test_with_valid_environ_path(self, monkeypatch):
            valid_path = os.getcwd()
            envs = {
                'token_path': valid_path
            }
            monkeypatch.setattr(os, 'environ', envs)
            path = get_token_file_path()
            assert path == valid_path

        def test_with_invalid_environ_path(self, monkeypatch):
            invalid_path = ''
            envs = {
                'token_path': invalid_path
            }
            monkeypatch.setattr(os, 'environ', envs)
            path = get_token_file_path()
            assert path == '/google_drive_api/src/token.pickle'

        def test_with_default_path(self):
            path = get_token_file_path()
            assert path == '/google_drive_api/src/token.pickle'

    class TestCreateDownloadPath(object):

        def test_existing_path(self):
            folder_path = os.getcwd()
            path = create_download_path(folder_path)
            assert isinstance(path, str)
            assert path == folder_path

        @patch('utils.create_download_path')
        def test_os_error(self, path_mock):
            path_mock.side_effect = OSError
            with pytest.raises(OSError):
                create_download_path('')

