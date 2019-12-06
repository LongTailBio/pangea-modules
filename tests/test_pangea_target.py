"""Test suite for s3 transfer manager."""

from unittest import TestCase
from os import getcwd, makedirs, environ, remove
from os.path import isfile, dirname, join
from random import randint
from time import sleep
from json import dumps

from functools import wraps

from pangea_modules import PangeaServerInterface, S3Uri, PangeaTarget


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


def with_server_interface(func):
    """Make a default AWS credential file in the home dir."""
    @wraps(func)
    def decorated_function(self, *args, **kwargs):
        server_interface = PangeaServerInterface.from_address(
            join(dirname(__file__), 'pangea_server_interface')
        )
        return func(self, server_interface, *args, **kwargs)

    return decorated_function


def with_clean_transfer_manager(func):
    """Make a default AWS credential file in the home dir."""
    @wraps(func)
    def decorated_function(self, *args, **kwargs):
        transfer_filepath = join(
            dirname(__file__),
            'pangea_server_interface',
            'transfer_manager_status.json'
        )
        with open(transfer_filepath, 'w') as tf:
            tf.write('{}')
        return func(self, *args, **kwargs)

    return decorated_function


SERVER_ADDRESS = join(dirname(__file__), 'pangea_server_interface')


class TestPangeaTarget(TestCase):
    """Test suite for wasabi."""

    @with_server_interface
    def test_get_data_target(self, server_interface):
        target = PangeaTarget(
            SERVER_ADDRESS,
            'group_name',
            'sample_name',
            'module_name',
            'field_2'
        )  # The field name is based on the output of the mock server.
           # `field_2` is data. `field_3` is an s3_uri with a real file.
        self.assertTrue(target.exists())
        self.assertIn('value_1', target.payload)

    @with_aws_credentials
    @with_clean_transfer_manager
    @with_server_interface
    def test_get_file_target(self, server_interface):
        target = PangeaTarget(
            SERVER_ADDRESS,
            'group_name',
            'sample_name',
            'module_name',
            'field_3',
            is_s3=True
        )  # The field name is based on the output of the mock server.
           # `field_2` is data. `field_3` is an s3_uri with a real file.
        self.assertTrue(target.exists())
        local_path = target.local_path(sleep_time=0.1)
        self.assertTrue(isfile(local_path))
        self.assertTrue(len(open(local_path).read()) > 0)
        remove(local_path)
