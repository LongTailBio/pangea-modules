
import requests

from sys import stderr

from .token_auth import TokenAuth


class Knex:
    """Knex wraps MetaGenScope requests requiring authentication."""

    def __init__(self, token_auth, host, headers=None):
        """Instantiate Knex instance."""
        self.auth = token_auth
        self.host = host

        self.headers = headers
        if self.headers is None:
            self.headers = {'Accept': 'application/json'}

    def post(self, endpoint, payload):
        """Perform authenticated POST request."""
        url = self.host + endpoint
        if payload:
            response = requests.post(url,
                                     headers=self.headers,
                                     auth=self.auth,
                                     json=payload)
        else:
            response = requests.post(url, headers=self.headers, auth=self.auth)
        if response.status_code >= 400:
            print(response.content, file=stderr)
        return response.json()

    def get(self, endpoint):
        """Perform authenticated GET request."""
        url = self.host + endpoint
        response = requests.get(url,
                                headers=self.headers,
                                auth=self.auth)
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint):
        """Perform authenticated DELETE request."""
        url = self.host + endpoint
        response = requests.delete(url,
                                   headers=self.headers,
                                   auth=self.auth)
        response.raise_for_status()
        return response.json()

    @classmethod
    def from_jwt_token(cls, jwt_token, host, headers=None):
        token_auth = TokenAuth(jwt_token)
        return cls(token_auth, host, headers=headers)
