import chardet
import sys

_ver = sys.version_info

is_py2 = _ver[0] == 2
is_py3 = _ver[0] == 3

if is_py2:
    from urlparse import urlunparse, urlparse
    from urllib import urlencode, quote
    import mock
    import urllib2
    from urllib2 import URLError
    import json as json_p
    import datetime
    import ssl

    class PutRequest(urllib2.Request):
        def get_method(self, *args, **kwargs):
            return "PUT"

    class DeleteRequest(urllib2.Request):
        def get_method(self, *args, **kwargs):
            return "DELETE"

    class Response(urllib2.URLError):
        def __init__(self, r):
            super(urllib2.URLError, self).__init__()
            self._content = False
            self._content_consumed = False
            self._next = None
            self.headers = r.info()
            self.raw = None
            self.url = None
            self.encoding = None
            self.history = []
            self.reason = None
            # self.cookies = cookiejar_from_dict({})
            self.elapsed = datetime.timedelta(0)
            self.request = None
            self.status_code = r.getcode()
            self.json_obj = r.read()
            self.url = r.geturl()

        def json(self):
            return json_p.loads(self.json_obj)

        def raise_for_status(self):
            http_error_msg = ""
            if isinstance(self.reason, bytes):
                try:
                    reason = self.reason.decode("utf-8")
                except UnicodeDecodeError:
                    reason = self.reason.decode("iso-8859-1")
            else:
                reason = self.reason

            if 400 <= self.status_code < 500:
                http_error_msg = u"%s Client Error: %s for url: %s" % (
                    self.status_code,
                    reason,
                    self.url,
                )

            elif 500 <= self.status_code < 600:
                http_error_msg = u"%s Server Error: %s for url: %s" % (
                    self.status_code,
                    reason,
                    self.url,
                )

            if http_error_msg:
                raise urllib2.URLError(http_error_msg, response=self)

    class Requests:
        def get(self, url, headers=None, json=None):
            if headers is None:
                headers = {}
            request = urllib2.Request(url, headers=headers)
            try:
                response = urllib2.urlopen(request)
            except URLError as e:
                raise URLError(e)
            return Response(response)

        def post(self, url, headers=None, json=None, data=None):
            if headers is None:
                headers = {}
            if not data:
                headers.update(
                    {"Content-type": "application/json", "Accept": "text/plain"}
                )
                request = urllib2.Request(url, data=json_p.dumps(json), headers=headers)
            else:
                request = urllib2.Request(url, data=data, headers=headers)
                
            try:
                response = urllib2.urlopen(request)
            except URLError as e:
                raise URLError(e)
                
            return Response(response)

        def put(self, url, headers=None, json=None):
            if headers is None:
                headers = {}
            headers.update({"Content-type": "application/json", "Accept": "text/plain"})
            request = PutRequest(url, data=json_p.dumps(json), headers=headers)
            try:
                response = urllib2.urlopen(request)
            except URLError as e:
                raise URLError(e)
            return Response(response)

        def delete(self, url, headers=None, json=None):
            if headers is None:
                headers = {}
            headers.update({"Content-type": "application/json", "Accept": "text/plain"})
            request = DeleteRequest(url, data=json_p.dumps(json), headers=headers)
            try:
                response = urllib2.urlopen(request)
            except URLError as e:
                raise URLError(e)
            return Response(response)

    requests = Requests()


elif is_py3:
    from urllib.parse import urlunparse, urlparse, urlencode, quote
    from urllib.error import URLError
    from unittest import mock
    import requests
