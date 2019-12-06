
from os import environ
from os.path import join

CONFIG_AUTH_SECTION = 'pangea_server'
CONFIG_AUTH_JWT_TOKEN = 'token'
CONFIG_AUTH_HOST = 'host'
CONFIG_S3_SECTION = 's3'
CONFIG_S3_ENDPOINT_URL = 'endpoint_url'
CONFIG_S3_PROFILE_NAME = 'profile_name'
CONFIG_LOCAL_FS_SECTION = 'local_file_system'
CONFIG_LOCAL_FS_PATH_PREFIX = 'path_prefix'
CONFIG_LOCAL_FS_PATH_TEMPLATE = 'path_template'

TRANSFER_MANAGER_FILENAME = 'transfer_manager_status.json'
CONFIG_FILENAME = 'pangea_config.ini'

DEFAULT_CONFIG_LOCATION = join(
    environ['HOME'], '.pangea_modules', CONFIG_FILENAME
)
