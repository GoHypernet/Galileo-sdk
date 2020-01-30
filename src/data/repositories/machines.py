from urllib.parse import urlunparse

import requests


class MachinesRepository:
    def __init__(self, settings_repository, access_token):
        self._settings_repository = settings_repository
        self._access_token = access_token
        self._headers = {"Authorization": f"Bearer {self._access_token}"}

    def _make_url(self, endpoint, params="", query="", fragment=""):
        settings = self._settings_repository.get_settings()
        backend = settings.backend
        schema, addr = backend.split("://")
        return urlunparse((schema, backend, endpoint, params, query, fragment))

    def _request(self, request, endpoint, data=None, params="", query="", fragment=""):
        url = self._make_url(endpoint, params, query, fragment)
        return request(url, json=data, headers=self._headers)

    def _get(self, *args, **kwargs):
        return self._request(requests.get, *args, **kwargs)

    def _put(self, *args, **kwargs):
        return self._request(requests.put, *args, **kwargs)

    def get_machine_by_id(self, machine_id):
        """
        Get machine's info by its id

        :param machine_id: machines id
        :return: response with an object of machine info
        """
        return self._get(f"/machines/{machine_id}")

    def list_machines(self, page=1, items=25, mids=None, userids=None):
        """
        List all machines

        :param page: optional, page #
        :param items: optional, items per page
        :param mids: optional, filter by machine id
        :param userids: optional, filter by user id
        :return: {'machines': [<machines>]}
        """
        return self._get("/machines", {page, items, mids, userids})

    def update_max_concurrent_jobs(self, mid, amount):
        """
        Update the number of allowed concurrent jobs for a machine

        :param mid: machine's id
        :param amount: number of allowed concurrent jobs
        :return:
        """
        return self._put(f"/machines/{mid}/update_max", {amount})
