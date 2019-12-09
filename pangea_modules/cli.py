
import click

from os import environ
from os.path import join

from .network.authenticator import Authenticator
from .network.constants import (
    CONFIG_FILENAME,
    DEFAULT_CONFIG_LOCATION,
    CONFIG_AUTH_SECTION,
    CONFIG_AUTH_JWT_TOKEN,
)


@click.group()
def main():
    pass


@main.command('set-config')
@click.option('-p', '--path', default=DEFAULT_CONFIG_LOCATION)
def set_config(path):
    """What do I actually want this fucntion to do?"""
    pass


@main.command('login')
@click.option('-y/-n', '--yes/--no', default=False)
@click.option('-h', '--host', default=None)
@click.option('-c', '--config-path', default=DEFAULT_CONFIG_LOCATION, type=click.Path())
@click.argument('user_email')
@click.argument('password')
def login(yes, host, config_path, user_email, password):
    """Authenticate as an existing MetaGenScope user."""
    if host is None:
        host = environ['PANGEA_HOST']

    try:
        jwt_token = Authenticator(host=host).login(user_email, password)
        if yes or click.confirm('Store token for future use (overwrites existing)?'):
            config = configparser.ConfigParser().read(config_path)
            config[CONFIG_AUTH_SECTION][CONFIG_AUTH_JWT_TOKEN] = jwt_token
            with open(config_path, 'w') as configfile:
                self.config.write(configfile)
            click.echo('Token stored.', err=True)
    except HTTPError as http_error:
        click.echo(
            f'There was an error with registration:\n{http_error}',
            err=True
        )
