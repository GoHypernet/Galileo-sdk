from typing import List, Optional
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
        return urlunparse((schema, addr, endpoint, params, query, fragment))

    def _request(self, request, endpoint, data=None, params="", query="", fragment=""):
        url = self._make_url(endpoint, params, query, fragment)
        return request(url, json=data, headers=self._headers)

    def _get(self, *args, **kwargs):
        return self._request(requests.get, *args, **kwargs)

    def _put(self, *args, **kwargs):
        return self._request(requests.put, *args, **kwargs)

    def get_machine_by_id(self, machine_id: str):
        """
        Get machine's info by its id

        :param machine_id: machines id
        :return: response with an object of machine info
        """
        return self._get(f"/machines/{machine_id}")

    def list_machines(
        self,
        mids: Optional[List[str]] = None,
        userids: Optional[List[str]] = None,
        page: Optional[int] = 1,
        items: Optional[int] = 25,
    ):
        """
        List all machines

        :param page: optional, page #
        :param items: optional, items per page
        :param mids: optional, filter by machine id
        :param userids: optional, filter by user id
        :return: {'machines': [<machines>]}
        """
        return self._get(
            "/machines",
            {"page": page, "items": items, "mids": mids, "userids": userids},
        )

    def update_max_concurrent_jobs(self, mid: str, amount: int):
        """
        Update the number of allowed concurrent jobs for a machine

        :param mid: machine's id
        :param amount: number of allowed concurrent jobs
        :return:
        """
        return self._put(f"/machines/{mid}/update_max", {"amount": amount})
