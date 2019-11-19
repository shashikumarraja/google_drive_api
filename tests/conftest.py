"""
contains fixtures to be used in tests
"""
import os
from os import path
from os.path import join
import json
import pytest
import logging
import allure

logger = logging.getLogger(__name__)
@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """ create and set allure report directory to store test run result
    """
    if config.option.allure_report_dir is None:
        directory = join(os.getcwd(), 'tests/reports/')
        if not path.exists(directory):
            try:
                os.makedirs(directory)
            except OSError as error:
                logger.error(error)
                raise Exception('Unable to create report dir:%s' % error)
        config.option.allure_report_dir = directory
    else:
        logger.info('Report path already set!!!')