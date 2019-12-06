"""Test suite for s3 transfer manager."""

from unittest import TestCase
from os import getcwd, makedirs, environ, remove
from os.path import isfile, dirname, join
from random import randint
from time import sleep
from json import dumps

from functools import wraps

from pangea_modules import PangeaServerInterface


def with_aws_credentials(func):
    """Make a default AWS credential file in the home dir."""
    @wraps(func)
    def decorated_function(self, *args, **kwargs):
        cred_filename = environ['HOME'] + '/.aws/credentials'
        if isfile(cred_filename):
            return func(self, *args, **kwargs)
        makedirs(dirname(cred_filename), exist_ok=True)
        access_key, secret_key = environ['AWS_ACCESS_KEY'], environ['AWS_SECRET_ACCESS_KEY']
        creds = f'[default]\naws_access_key_id={access_key}\naws_secret_access_key={secret_key}\n'
        creds += f'[wasabi]\naws_access_key_id={access_key}\naws_secret_access_key={secret_key}\n'
        with open(cred_filename, 'w') as cf:
            cf.write(creds)

        return func(self, *args, **kwargs)

    return decorated_function


def with_download_manager(func):
    """Make a default AWS credential file in the home dir."""
    @wraps(func)
    def decorated_function(self, *args, **kwargs):
        server_interface = PangeaServerInterface.from_address(
            join(dirname(__file__), 'pangea_server_interface')
        )
        return func(self, server_interface.download_manager, *args, **kwargs)

    return decorated_function


class TestS3TransferManager(TestCase):
    """Test suite for wasabi."""

    @with_aws_credentials
    @with_download_manager
    def test_download_file_blocking(self, download_manager):
        uri_str = 's3://metasub/Scripts/downloadem.sh'
        download_manager.download(uri_str, force=True, block=True)
        local_path = download_manager.local_path(uri_str)
        self.assertTrue(isfile(local_path))
        self.assertTrue(len(open(local_path).read()) > 0)
        remove(local_path)

    @with_aws_credentials
    @with_download_manager
    def test_download_file(self, download_manager):
        uri_str = 's3://metasub/Scripts/downloadem.sh'
        download_manager.download(uri_str, force=True)
        local_path = download_manager.local_path(uri_str)
        while not local_path:
            sleep(1)
            local_path = download_manager.local_path(uri_str)
        self.assertTrue(isfile(local_path))
        self.assertTrue(len(open(local_path).read()) > 0)
        remove(local_path)
