
from time import sleep


class S3Uri:

    def __init__(self, endpoint_url, uri_str, download_manager):
        self.endpoint_url = endpoint_url
        self.uri_str = uri_str
        self.download_manager = download_manager

    def local_path(self, sleep_time=10):
        """Return the local path to this file.

        Blocks till download is complete.
        """
        mypath = self.download_manager.local_path(self.uri_str)
        while mypath is None:
            sleep(sleep_time)  # sleep for ten seconds as files are likely to be big
            mypath = self.download_manager.local_path(self.uri_str)
        return mypath

    def exists_on_s3(self):
        return self.download_manager.exists(self.uri_str)

    def upload(self):
        pass

    def serializable(self):
        return {
            'endpoint_url': self.endpoint_url,
            'uri': self.uri_str,
        }

    @classmethod
    def from_dict(cls, field, download_manager):
        return S3Uri(
            field['endpoint_url'],
            field['uri'],
            download_manager
        )
