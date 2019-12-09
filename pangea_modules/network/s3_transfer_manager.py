
from json import loads, dumps
from boto3.s3.transfer import TransferConfig
import boto3
import botocore
from threading import Thread
from os.path import isfile, join, dirname
from os import makedirs

try:
    from urlparse import urlsplit
except ImportError:
    from urllib.parse import urlsplit

from .file_lock import FileLock
from .constants import (
    CONFIG_LOCAL_FS_SECTION,
    CONFIG_LOCAL_FS_PATH_PREFIX,
    CONFIG_LOCAL_FS_PATH_TEMPLATE,
)

NO_STATUS = 'NO_STATUS'
UPLOAD_COMPLETE = 'UPLOAD_COMPLETE'
DOWNLOAD_COMPLETE = 'DOWNLOAD_COMPLETE'
UPLOAD_IN_PROGRESS = 'UPLOAD_IN_PROGRESS'
DOWNLOAD_IN_PROGRESS = 'DOWNLOAD_IN_PROGRESS'
UPLOAD_PART_SIZE = 8388608  # 8MB


class S3TransferManager:
    """Centralized transferer for files from S3.

    Main use is to avoid double downloading files.
    """

    def __init__(self, endpoint_url, profile_name, status_filepath, config):
        self.file_lock = FileLock(status_filepath)
        self.status_filepath = status_filepath
        self.session = boto3.Session(profile_name=profile_name)
        self.endpoint_url = endpoint_url
        self.s3 = self.session.resource('s3', endpoint_url=endpoint_url)
        self.config = config

    def _build_local_path(self, uri_str):
        """Return a local path to be used for a given URI."""
        path_string = join(
            self.config[CONFIG_LOCAL_FS_SECTION][CONFIG_LOCAL_FS_PATH_PREFIX],
            self.config[CONFIG_LOCAL_FS_SECTION].get(
                CONFIG_LOCAL_FS_PATH_TEMPLATE,
                '<bucket_name>/<key>'
            )
        )
        bucket, key = self._path_to_bucket_and_key(uri_str)
        path_string = path_string.replace('<bucket_name>', bucket)
        path_string = path_string.replace('<key>', key)
        return path_string

    def _get_status(self, uri_str):
        with self.file_lock:
            status_dict = loads(open(self.status_filepath).read())
            current_status = status_dict.get(uri_str, {'status': NO_STATUS, 'local_path': ''})
            return current_status

    def _change_status(self, uri_str, status, local_path=None):
        with self.file_lock:
            status_dict = loads(open(self.status_filepath).read())
            current_status = status_dict.get(uri_str, {'status': NO_STATUS, 'local_path': ''})
            if status:
                current_status['status'] = status
            if local_path:
                current_status['local_path'] = local_path
            status_dict[uri_str] = current_status
            with open(self.status_filepath, 'w') as sf:
                sf.write(dumps(status_dict))

    def exists(self, path):
        (bucket, key) = self._path_to_bucket_and_key(path)
        try:
            self.s3.Object(bucket, key).load()
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] in ['NoSuchKey', '404']:
                return False
            else:
                raise
        return True

    @staticmethod
    def _path_to_bucket_and_key(path):
        (_, netloc, path, query, _) = urlsplit(path, allow_fragments=False)
        question_mark_plus_query = '?' + query if query else ''
        path_without_initial_slash = path[1:] + question_mark_plus_query
        return netloc, path_without_initial_slash

    def _put_multipart(self, local_path, uri_str, part_size=UPLOAD_PART_SIZE, **kwargs):
        """Put an object stored locally to an S3 path using S3 multi-part upload (for files > 8Mb).
        :param local_path: Path to source local file
        :param uri_str: URL for target S3 location
        :param part_size: Part size in bytes. Default: 8388608 (8MB)
        :param kwargs: Keyword arguments passed to the boto function `upload_fileobj` as ExtraArgs
        """
        (bucket, key) = self._path_to_bucket_and_key(uri_str)
        self.s3.meta.client.upload_fileobj(
            Fileobj=open(local_path, 'rb'),
            Bucket=bucket,
            Key=key,
            Config=TransferConfig(multipart_chunksize=part_size),
            ExtraArgs=kwargs
        )

    def upload(self, local_path, uri_str):
        """Start an upload of the local_path to the uri. No return."""
        current_status = self._get_status(uri_str)['status']
        if current_status in (UPLOAD_IN_PROGRESS, UPLOAD_COMPLETE):
            return
        assert current_status == NO_STATUS
        self._change_status(uri_str, UPLOAD_IN_PROGRESS)

        def threaded_upload():
            self._put_multipart(local_path, uri_str)
            self._change_status(uri_str, UPLOAD_COMPLETE)

        Thread(target=threaded_upload).start()

    def is_uploaded(self, local_path, uri_str):
        """Return True if the upload is complete else False."""
        current_status = self._get_status(uri_str)
        if current_status['status'] == UPLOAD_COMPLETE:
            assert local_path == current_status['local_path']
            return True
        elif current_status['status'] == UPLOAD_IN_PROGRESS:
            assert local_path == current_status['local_path']
            return False
        return False

    def download(self, uri_str, force=False, block=False):
        """Start a download of the given file from S3. No return."""
        current_status = self._get_status(uri_str)['status']
        if not force and current_status in (DOWNLOAD_IN_PROGRESS, DOWNLOAD_COMPLETE):
            return
        assert force or current_status == NO_STATUS
        self._change_status(uri_str, DOWNLOAD_IN_PROGRESS)

        def threaded_download():
            (bucket, key) = self._path_to_bucket_and_key(uri_str)
            local_path = self._build_local_path(uri_str)
            makedirs(dirname(local_path), exist_ok=True)
            self.s3.meta.client.download_file(bucket, key, local_path)
            self._change_status(uri_str, DOWNLOAD_COMPLETE, local_path=local_path)

        if block:
            threaded_download()
        else:
            Thread(target=threaded_download).start()

    def local_path(self, uri_str):
        """Return the local path for the given file or None if not downloaded.

        Start downloading the file if not already doing so.
        """
        current_status = self._get_status(uri_str)
        if current_status['status'] == DOWNLOAD_COMPLETE:
            assert isfile(current_status['local_path'])
            return current_status['local_path']
        elif current_status['status'] != DOWNLOAD_IN_PROGRESS:
            self.download(uri_str)
            return None
        return None
