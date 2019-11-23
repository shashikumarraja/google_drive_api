"""
Unit Tests for src/drive.api.py functions
"""
import random
import pytest
from jsonschema import validate
from googleapiclient.discovery import Resource
from googleapiclient.http import HttpRequest
from drive_api import get_drive_service, call_export_api, call_file_info_api, call_get_media_api, get_drive_file_names, download_file_from_drive, get_extension_types
from credentials import get_credential


class TestDriveApi(object):

    function_list = [get_drive_service, call_export_api, call_file_info_api,
                     call_get_media_api, get_drive_file_names, download_file_from_drive, get_extension_types]
    creds = get_credential()
    service = get_drive_service(creds)
    mime_types = ['application/vnd.google-apps.presentation',
                  'application/vnd.google-apps.spreadsheet',
                  'application/vnd.google-apps.document']

    @pytest.mark.parametrize('function_name', function_list)
    def test_callable(self, function_name, logger):
        """
        Verify that functions are callable
        """
        assert callable(function_name)

    def test_get_drive_service(self):
        creds = TestDriveApi.creds
        res = get_drive_service(creds)
        assert isinstance(res, Resource)

    class TestGetDriveFileNames(object):
        def test_get_drive_file_names(self):
            res = get_drive_file_names(TestDriveApi.creds)
            assert isinstance(res, list)

    class TestCallFileInfoApi(object):
        def test_response_schema(self, load_json_schema):
            res = call_file_info_api(TestDriveApi.service)
            schema = load_json_schema('file_info.json')
            validate(res, schema)

    class TestCallExportApi(object):
        def test_return_type(self, fake):
            file_id = fake.md5(raw_output=False)
            mime_type = random.choice(TestDriveApi.mime_types)
            res = call_export_api(TestDriveApi.service,
                                  file_id, get_extension_types(), mime_type)
            assert isinstance(res, HttpRequest)

    class TestCallGetMediaApi(object):
        def test_return_type(self, fake):
            file_id = fake.md5(raw_output=False)
            res = call_get_media_api(TestDriveApi.service, file_id)
            assert isinstance(res, HttpRequest)

    class TestDownloadFileFromDrive(object):
        def test_return_type(self):
            res, message = download_file_from_drive()
            assert isinstance(res, bool)
            assert isinstance(message, str)
            assert res == True
            assert message == 'Success'