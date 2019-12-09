
import configparser
import json

from os import makedirs
from os.path import join, isfile, dirname

from .knex import Knex
from .s3_uri import S3Uri, LocalS3Uri
from .s3_transfer_manager import S3TransferManager
from .constants import (
    CONFIG_AUTH_SECTION,
    CONFIG_AUTH_HOST,
    CONFIG_AUTH_JWT_TOKEN,
    CONFIG_S3_SECTION,
    CONFIG_S3_ENDPOINT_URL,
    CONFIG_S3_PROFILE_NAME,
    TRANSFER_MANAGER_FILENAME,
    CONFIG_FILENAME,
    CONFIG_LOCAL_FS_SECTION,
    CONFIG_LOCAL_FS_PATH_PREFIX,
    CONFIG_LOCAL_FS_PATH_TEMPLATE,
)

AR_NAME_URL = '/api/v1/analysis_results/byname'


class PangeaServerInterface:

    def __init__(self, knex, download_manager):
        self.knex = knex
        self.download_manager = download_manager

    def get_s3_uri(self, group_name, sample_name, module_name, field_name, ext=''):
        """Return an S3Uri for the given params."""
        url = f'{AR_NAME_URL}/{group_name}/{sample_name}/{module_name}/{field_name}/s3uri'
        if ext:
            url += f'?ext={ext}'
        response = self.knex.get(url)['data']
        field = S3Uri.from_dict(response, self.download_manager)
        return field

    def load_result_field(self, group_name, sample_name, module_name, field_name, field_value):
        """Load the field into the Pangea database."""
        payload = field_value
        if isinstance(payload, S3Uri):
            payload.upload()
            payload = payload.serializable()
        url = f'{AR_NAME_URL}/{group_name}/{sample_name}/{module_name}/{field_name}'
        response = self.knex.post(url, payload)
        return response

    def find_result_field(self, group_name, sample_name, module_name, field_name):
        """Check for relevant result field in the db. Return the payload
        if it exists else None. If payload is S3 return as an S3Uri"""
        url = f'{AR_NAME_URL}/{group_name}/{sample_name}/{module_name}'
        response = self.knex.get(url)['data']
        field = response[field_name]
        try:
            if '__type__' in field and field['__type__'].lower() == 's3_uri':
                field = S3Uri.from_dict(field, self.download_manager)
        except TypeError:
            pass
        return field

    def get_group_s3_uri(self, group_name, module_name, field_name, ext=''):
        """Return an S3Uri for the given params."""
        url = f'{AR_NAME_URL}/group/{group_name}/{module_name}/{field_name}/s3uri'
        if ext:
            url += f'?ext={ext}'
        response = self.knex.get(url)['data']
        field = S3Uri.from_dict(response, self.download_manager)
        return field

    def load_group_result_field(self, group_name, module_name, field_name, field_value):
        """Load the field into the Pangea database."""
        payload = field_value
        if isinstance(payload, S3Uri):
            payload.upload()
            payload = payload.serializable()
        url = f'{AR_NAME_URL}/group/{group_name}/{module_name}/{field_name}'
        response = self.knex.post(url, payload)
        return response

    def find_group_result_field(self, group_name, module_name, field_name):
        """Check for relevant result field in the db. Return the payload
        if it exists else None. If payload is S3 return as an S3Uri"""
        url = f'{AR_NAME_URL}/group/{group_name}/{module_name}'
        response = self.knex.get(url)['data']
        field = response[field_name]
        try:
            if '__type__' in field and field['__type__'].lower() == 's3_uri':
                field = S3Uri.from_dict(field, self.download_manager)
        except TypeError:
            pass
        return field

    def get_samples_in_group(self, group_name):
        """Return a list of the samples in the specified group."""
        assert False

    @classmethod
    def from_address(cls, server_address):
        config = configparser.ConfigParser()
        config.read(join(server_address, CONFIG_FILENAME))
        knex = Knex.from_jwt_token(
            config[CONFIG_AUTH_SECTION][CONFIG_AUTH_JWT_TOKEN],
            config[CONFIG_AUTH_SECTION][CONFIG_AUTH_HOST]
        )
        transfer_manager = S3TransferManager(
            config[CONFIG_S3_SECTION][CONFIG_S3_ENDPOINT_URL],
            config[CONFIG_S3_SECTION][CONFIG_S3_PROFILE_NAME],
            join(server_address, TRANSFER_MANAGER_FILENAME),
            config=config
        )
        return cls(knex, transfer_manager)


class LocalPangeaServerInterface:
    """Oxymoronic name this class proxies
    a server for local pipelines but never
    actually uses the internet.
    """

    def __init__(self, config):
        self.config = config

    def _build_local_path(self, group_name, sample_name, module_name, field_name, ext=''):
        path_string = join(
            self.config[CONFIG_LOCAL_FS_SECTION][CONFIG_LOCAL_FS_PATH_PREFIX],
            self.config[CONFIG_LOCAL_FS_SECTION].get(
                CONFIG_LOCAL_FS_PATH_TEMPLATE,
                '<bucket_name>/<kind>/<key>'
            )
        )
        if ext and ext[0] != '.':
            ext = '.' + ext
        path_string = path_string.replace('<bucket_name>', group_name)
        path_string = path_string.replace('<kind>', 'samples')
        key = (
            f'{sample_name}/{module_name}/'
            f'{group_name}.{sample_name}.{module_name}.{field_name}{ext}'
        )
        path_string = path_string.replace('<key>', key)
        return path_string

    def get_s3_uri(self, group_name, sample_name, module_name, field_name, ext=''):
        """Return an S3Uri for the given params."""
        local_path = self._build_local_path(
            group_name, sample_name, module_name, field_name, ext=ext
        )
        field = LocalS3Uri(local_path)
        return field

    def load_result_field(self, group_name, sample_name, module_name, field_name, field_value):
        """Write a file locally containing the field_value. Return the filepath."""
        if isinstance(field_value, S3Uri):
            field_value = field_value.serializable()
        local_path = self._build_local_path(
            group_name, sample_name, module_name, field_name, ext='pangea.json'
        )
        makedirs(dirname(local_path), exist_ok=True)
        with open(local_path, 'w') as lp:
            lp.write(json.dumps(field_value))
        return None

    def find_result_field(self, group_name, sample_name, module_name, field_name):
        """Check for relevant result field in the filesystem. Return the payload
        if it exists else None. If payload is S3 return as an S3Uri"""
        local_path = self._build_local_path(
            group_name, sample_name, module_name, field_name, ext='pangea.json'
        )
        if not isfile(local_path):
            return None
        field = json.loads(open(local_path).read())
        try:
            if '__type__' in field and field['__type__'].lower() == 's3_uri':
                field = LocalS3Uri.from_dict(field)
        except TypeError:
            pass
        return field

    def get_group_s3_uri(self, group_name, module_name, field_name, ext=''):
        """Return an S3Uri for the given params."""
        assert False

    def load_group_result_field(self, group_name, module_name, field_name, field_value):
        """Write a file locally containing the field_value. Return the filepath."""
        assert False

    def find_group_result_field(self, group_name, module_name, field_name):
        """Check for relevant result field in the filesystem. Return the payload
        if it exists else None. If payload is S3 return as an S3Uri"""
        assert False

    def get_samples_in_group(self, group_name):
        """Return a list of the samples in the specified group."""
        path_string = join(
            self.config[CONFIG_LOCAL_FS_SECTION][CONFIG_LOCAL_FS_PATH_PREFIX],
            f'{group_name}/sample_list.txt'
        )
        out = []
        with open(path_string) as f:
            for line in f:
                line = line.strip()
                if line:
                    out.append(line)
        return out

    @classmethod
    def from_address(cls, server_address):
        config = configparser.ConfigParser()
        config.read(join(server_address, CONFIG_FILENAME))
        return cls(config)
