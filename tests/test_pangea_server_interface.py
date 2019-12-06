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


def with_server_interface(func):
    """Make a default AWS credential file in the home dir."""
    @wraps(func)
    def decorated_function(self, *args, **kwargs):
        server_interface = PangeaServerInterface.from_address(
            join(dirname(__file__), 'pangea_server_interface')
        )
        return func(self, server_interface, *args, **kwargs)

    return decorated_function


class TestPangeaServerInterface(TestCase):
    """Test suite for wasabi."""

    @with_aws_credentials
    @with_server_interface
    def test_get_s3_uri(self, server_interface):
        s3_uri = server_interface.get_s3_uri(
            'my_group_name',
            'my_sample_name',
            'my_module_name',
            'my_field_name'
        )
        for el in ['my_group_name', 'my_sample_name', 'my_module_name', 'my_field_name']:
            self.assertIn(el, s3_uri.uri_str)
