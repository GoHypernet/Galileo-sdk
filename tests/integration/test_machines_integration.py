from src import GalileoSdk
import os

# Must set env variables before running tests
USERNAME = os.getenv("GALILEO_USER")
PASSWORD = os.getenv("GALILEO_PASSWORD")
CONFIG = "development"

galileo = GalileoSdk(username=USERNAME, password=PASSWORD, config=CONFIG,)


def test_list_machines():
    machine_list = galileo.machines.list_machines()
    assert not machine_list == None
    assert "arch" in machine_list["machines"][0]
    assert "cpu" in machine_list["machines"][0]
    assert "gpu" in machine_list["machines"][0]


def test_get_machines_by_id():
    machine = galileo.machines.get_machines_by_id("3110b6151b2d44f8a6ed0c84e960c127")
    assert not machine == None
    assert "arch" in machine
    assert "cpu" in machine
    assert "name" in machine


def test_update_concurrent_max_jobs():
    r = galileo.machines.update_concurrent_max_jobs(
        "3110b6151b2d44f8a6ed0c84e960c127", 10
    )
    assert r == True
