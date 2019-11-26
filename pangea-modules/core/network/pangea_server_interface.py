
from .s3_uri import S3Uri

AR_NAME_URL = '/api/v1/analysis_results/byname'


class PangeaServerInterface:

    def __init__(self, knex, download_manager):
        self.knex = knex
        self.download_manager = download_manager

    def get_s3_uri(self, group_name, sample_name, module_name, field_name):
        """Return an S3Uri for the given params."""
        url = f'{AR_NAME_URL}/{group_name}/{sample_name}/{module_name}/{field_name}/s3uri'
        response = self.knex.get(url)
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
        response = self.knex.get(url)
        field = response[field_name]
        if '__type__' in field and field['__type__'].lower() == 's3_uri':
            field = S3Uri.from_dict(field, self.download_manager)
        return field
