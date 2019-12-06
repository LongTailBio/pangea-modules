
import luigi
import os

from .network import PangeaServerInterface, S3Uri


class PangeaTarget(luigi.Target):
    """Target for luigi that corresponds to an
    AnalysisResultField for Pangea Server.

    """

    def __init__(
        self,
        server_address, group_name, sample_name, module_name, field_name,
        is_s3=False, local_path=None, payload=None, force_rebuild=False
    ):
        self.group_name = group_name
        self.sample_name = sample_name
        self.module_name = module_name
        self.field_name = field_name
        self.is_s3 = is_s3
        self.force_rebuild = force_rebuild
        self.server = PangeaServerInterface.from_address(server_address)
        self.is_local_path = False
        if local_path:  # bit hacky
            self.is_s3 = True
            self.is_local_path = True
            self.payload = S3Uri(
                self.server.download_manager.endpoint_url,
                None,
                self.server.download_manager
            )
            self.payload._local_path = local_path
        elif payload:
            self.payload = payload
        else:
            self.payload = self.server.find_result_field(
                self.group_name, self.sample_name, self.module_name, self.field_name
            )
        if self.is_s3 and self.payload:
            assert isinstance(self.payload, S3Uri)

    def exists(self):
        if self.force_rebuild:
            return False
        if self.payload is None:
            return False
        if self.is_s3:
            return self.is_local_path or self.payload.exists_on_s3()
        return True

    def set_payload(self, value):
        """Set the payload for this target. Return self for convenience."""
        if self.is_s3:
            value = S3Uri(value, self.server.download_manager)
        self.payload = value
        return self

    def upload(self):
        assert self.payload
        field = self.payload
        if self.is_s3:
            field.upload()
            field = field.serializable()
        self.server.load_result_field(
            self.group_name,
            self.sample_name,
            self.module_name,
            self.field_name,
            field
        )
        return self

    def makedirs(self):
        """Create parent folders for the local path if they do not exist."""
        assert self.is_s3
        normpath = os.path.normpath(self.local_path())
        parentfolder = os.path.dirname(normpath)
        if parentfolder:
            try:
                os.makedirs(parentfolder)
            except OSError:
                pass

    def start_download(self):
        assert self.is_s3

    def local_path(self, sleep_time=10):
        assert self.is_s3
        return self.payload.local_path(sleep_time=sleep_time)
