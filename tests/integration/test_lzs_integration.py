from galileo_sdk import GalileoSdk

# Must set env variables before running tests
CONFIG = "development"

galileo = GalileoSdk(config=CONFIG)
lz_list = galileo.lz.list_lz()


def test_list_lzs():
    assert lz_list
    assert lz_list[0].arch
    assert lz_list[0].cpu_count
    assert lz_list[0].operating_system
    assert lz_list[0].gpu_count == 0


def test_get_lzs_by_id():
    lz = galileo.lz.get_lz_by_id(lz_list[0].lz_id)
    assert not lz == None
    assert lz.arch
    assert lz.cpu_count
    assert lz.name


galileo.disconnect()
