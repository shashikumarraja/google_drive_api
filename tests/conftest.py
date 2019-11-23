"""
contains fixtures to be used in tests
"""
import os
from os import path
from os.path import join, dirname
import json
import logging
import pytest
import logging
import allure
from faker import Faker

log = logging.getLogger(__name__) 

@pytest.fixture(scope="session")
def logger(request):
    """
    Expose logger to tests
    """
    return log

@pytest.fixture(scope="session")
def fake(request):
    """
    Expose faker to tests
    """
    fake = Faker()
    return fake

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """ 
    create and set allure report directory to store test run result
    """
    if config.option.allure_report_dir is None:
        directory = join(dirname(__file__), 'reports')
        if not path.exists(directory):
            try:
                os.makedirs(directory)
            except OSError as error:
                logger.error(error)
                raise Exception('Unable to create report dir:%s' % error)
        config.option.allure_report_dir = directory
    else:
        log.info('Report path already set!!!')

@pytest.fixture(scope='session')
def load_json_schema():
    """
    Reads the stored json schema file available at a given path
    """
    def _load_json_schema(filename):
        """ Loads the given schema file """
        relative_path = join('schema', filename)
        absolute_path = join(dirname(__file__), relative_path)
        if path.exists(absolute_path):
            with open(absolute_path) as schema_file:
                return json.loads(schema_file.read())
        else:
            log.error('Invalid schema file path: %s' % absolute_path)
    return _load_json_schema