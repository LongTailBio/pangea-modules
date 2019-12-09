
from os import getcwd, makedirs, environ, remove
from os.path import isfile, dirname, join
from random import randint
from time import sleep
from json import dumps

from functools import wraps

from pangea_modules import PangeaServerInterface, PangeaTarget


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
