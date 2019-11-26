
class S3TransferManager:
    """Centralized transferer for files from S3.

    Main use is to avoid double downloading files.
    """

    def upload(self, local_path, endpoint_url, uri_str):
        """Start an upload of the local_path to the uri. No return."""
        pass

    def is_uploaded(self, local_path, endpoint_url, uri_str):
        """Return True if the upload is complete else False."""
        pass

    def download(self, endpoint_url, uri_str):
        """Start a download of the given file from S3. No return."""
        pass

    def local_path(self, endpoint_url, uri_str):
        """Return the local path for the given file or None if not downloaded.

        Start downloading the file if not already doing so.
        """
        pass
