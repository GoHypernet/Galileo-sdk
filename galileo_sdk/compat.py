import chardet
import sys

_ver = sys.version_info

is_py2 = (_ver[0] == 2)
is_py3 = (_ver[0] == 3)

if is_py2:
    from urlparse import urlunparse
    import mock

elif is_py3:
    from urllib.parse import urlunparse
    from unittest import mock
