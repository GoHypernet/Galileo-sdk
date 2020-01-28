import requests
from urllib.parse import urlunparse


class ProfilesRepository:
    def __init__(self, settings_repository, access_token):
        self._settings_repository = settings_repository
        self._access_token = access_token
        self._headers = {'Authorization': f'Bearer {self._access_token}'}

    def _make_url(self, endpoint, params='', query='', fragment=''):
        settings = self._settings_repository.get_settings()
        backend = settings.backend
        schema, addr = backend.split('://')
        return urlunparse((schema, backend, endpoint, params, query, fragment))

    def _request(self, request, endpoint, data=None, params='', query='', fragment=''):
        url = self._make_url(endpoint, params, query, fragment)
        return request(url, json=data, headers=self._headers)

    def _get(self, *args, **kwargs):
        return self._request(requests.get, *args, **kwargs)

    def _post(self, *args, **kwargs):
        return self._request(requests.post, *args, **kwargs)

    def list_users(self, page, items):
        return self._get('/users', {page, items})
