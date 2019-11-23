"""
Unit Tests for src/drive.api.py functions
"""
import pytest
from jsonschema import validate
from googleapiclient.discovery import Resource
from drive_api import get_drive_service, call_export_api, call_file_info_api, call_get_media_api, get_drive_file_names, download_file_from_drive
from credentials import get_credential

class TestDriveApi(object):

    function_list = [get_drive_service, call_export_api, call_file_info_api, call_get_media_api, get_drive_file_names, download_file_from_drive]
    creds = get_credential()
    service = get_drive_service(creds)

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

    def test_get_drive_file_names(self):
        res = get_drive_file_names(TestDriveApi.creds)
        assert isinstance(res, list)

    def test_call_file_info_api(self, load_json_schema):
        res = call_file_info_api(TestDriveApi.service)
        schema = load_json_schema('file_info.json')
        validate(res, schema)




