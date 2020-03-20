from typing import Any, Callable, List, Optional
from urllib.parse import urlunparse

import requests

from galileo_sdk.business.objects.machines import (EMachineStatus, Machine,
                                                   UpdateMachineRequest)

from ..providers.auth import AuthProvider
from .settings import SettingsRepository


class MachinesRepository:
    def __init__(
        self,
        settings_repository: SettingsRepository,
        auth_provider: AuthProvider,
        namespace: str,
    ):
        self._settings_repository = settings_repository
        self._auth_provider = auth_provider
        self._namespace = namespace

    def _make_url(self, endpoint, params="", query="", fragment=""):
        settings = self._settings_repository.get_settings()
        backend = settings.backend
        schema, addr = backend.split("://")
        return urlunparse(
            (schema, f"{addr}{self._namespace}", endpoint, params, query, fragment,)
        )

    def _request(
        self,
        request: Callable,
        endpoint: str,
        data: Optional[Any] = None,
        params: Optional[str] = None,
        query: Optional[str] = None,
        fragment: Optional[str] = None,
    ):
        url = self._make_url(endpoint, params, query, fragment)
        access_token = self._auth_provider.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        r = request(url, json=data, headers=headers)
        r.raise_for_status()
        return r

    def _get(self, *args, **kwargs):
        return self._request(requests.get, *args, **kwargs)

    def _put(self, *args, **kwargs):
        return self._request(requests.put, *args, **kwargs)

    def get_machine_by_id(self, machine_id: str) -> Machine:
        response = self._get(f"/machines/{machine_id}")
        json: dict = response.json()
        return machine_dict_to_machine(json)

    def list_machines(self, query: str) -> List[Machine]:
        response = self._get("/machines", query=query)
        json: dict = response.json()
        machines: List[dict] = json["machines"]
        return [machine_dict_to_machine(machine) for machine in machines]

    def update(self, request: UpdateMachineRequest) -> Machine:
        response = self._put(
            f"/machines/{request.mid}",
            {
                "name": request.name,
                "gpu": request.gpu,
                "cpu": request.cpu,
                "os": request.os,
                "arch": request.arch,
                "memory": request.memory,
                "running_jobs_limit": request.running_jobs_limit,
                "active": request.active,
            },
        )
        json: dict = response.json()
        machine = json["machine"]
        return machine_dict_to_machine(machine)


def machine_dict_to_machine(machine: dict):
    return Machine(
        machine["name"],
        machine["userid"],
        EMachineStatus[machine["status"]],
        machine["mid"],
        machine["gpu"],
        machine["cpu"],
        machine["os"],
        machine["arch"],
        machine["memory"],
        machine["running_jobs_limit"],
    )
