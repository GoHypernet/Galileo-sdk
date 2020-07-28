from galileo_sdk.compat import urlunparse, requests


class RequestsRespository(object):
    def __init__(self, settings_repository, auth_provider, namespace):
        self._settings_repository = settings_repository
        self._auth_provider = auth_provider
        self._namespace = namespace

    def _make_url(self, endpoint, params="", query="", fragment=""):
        settings = self._settings_repository.get_settings()
        backend = settings.backend
        schema, addr = backend.split("://")
        return urlunparse(
            (
                schema,
                "{addr}{namespace}".format(addr=addr, namespace=self._namespace),
                endpoint,
                params,
                query,
                fragment,
            )
        )

    def _request(
        self, request, endpoint, data=None, params=None, query=None, fragment=None, files=None,
            filename=None
    ):
        url = self._make_url(endpoint, params, query, fragment)
        access_token = self._auth_provider.get_access_token()
        headers = {
            "Authorization": "Bearer {access_token}".format(access_token=access_token)
        }
        if files is None:
            r = request(url, json=data, headers=headers)
        else:
            headers["filename"] = filename
            headers["Content-Type"] = "application/octet-stream"
            r = request(url, json=data, headers=headers, data=files)
        r.raise_for_status()
        return r

    def _get(self, *args, **kwargs):
        return self._request(requests.get, *args, **kwargs)

    def _put(self, *args, **kwargs):
        return self._request(requests.put, *args, **kwargs)

    def _post(self, *args, **kwargs):
        return self._request(requests.post, *args, **kwargs)

    def _delete(self, *args, **kwargs):
        return self._request(requests.delete, *args, **kwargs)
