"""Test suite for s3 transfer manager."""

from unittest import TestCase
from os import remove
from os.path import isfile
from time import sleep

from .utils import (
    with_aws_credentials,
    with_download_manager,
)


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
