from galileo_sdk import GalileoSdk

# Must set env variables before running tests
CONFIG = "development"

galileo = GalileoSdk(config=CONFIG)
machine_list = galileo.machines.list_machines()


def test_list_machines():
    assert machine_list
    assert machine_list[0].arch
    assert machine_list[0].cpu_count
    assert machine_list[0].operating_system
    assert machine_list[0].gpu_count == 0


def test_get_machines_by_id():
    machine = galileo.machines.get_machines_by_id(machine_list[0].mid)
    assert not machine == None
    assert machine.arch
    assert machine.cpu_count
    assert machine.name


galileo.disconnect()
