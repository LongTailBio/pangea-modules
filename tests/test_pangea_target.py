"""Test suite for s3 transfer manager."""

from unittest import TestCase
from os import remove
from os.path import isfile

from pangea_modules import PangeaTarget

from .utils import (
    with_server_interface,
    with_aws_credentials,
    with_clean_transfer_manager,
)
from .constants import SERVER_ADDRESS


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
