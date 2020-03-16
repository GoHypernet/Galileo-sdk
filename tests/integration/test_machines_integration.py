import os

from galileo_sdk import GalileoSdk

# Must set env variables before running tests
CONFIG = "development"

galileo = GalileoSdk(config=CONFIG)
machine_list = galileo.machines.list_machines()


def test_list_machines():
    assert not machine_list == None
    assert "arch" in machine_list["machines"][0]
    assert "cpu" in machine_list["machines"][0]
    assert "gpu" in machine_list["machines"][0]


def test_get_machines_by_id():
    machine = galileo.machines.get_machines_by_id(machine_list["machines"][0]["mid"])
    assert not machine == None
    assert "arch" in machine
    assert "cpu" in machine
    assert "name" in machine


galileo.disconnect()
