"""Test suite for s3 transfer manager."""

from unittest import TestCase

from .utils import (
    with_aws_credentials,
    with_server_interface,
)


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
