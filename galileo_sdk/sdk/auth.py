from galileo_sdk.compat import requests
from datetime import datetime, timedelta
import os, urllib, json, webbrowser, time, tempfile

# wrapper class for Galileo sdk authentication. It automatically handles authentication for the user via the default webbrowser
class AuthSdk:
    def __init__(self, client_id="oDmH6Nf4DN3oILcNk7cQqBchXUfv7fpD", mode='prod', audience=''):
        self.domain = "https://galileoapp.auth0.com"
        self.headers_default = {'content-type': 'application/x-www-form-urlencoded'}
        self.client_id = client_id

        # if a custom audience is supplied, use it
        if audience:
            self.audience = audience
        else:
            # otherwise the choice is between production and development
            if mode == 'prod':
                self.audience = "https://booming-client-217619.appspot.com"
            elif mode == 'dev':
                self.audience = "https://profound-ripsaw-232522.appspot.com"
            else:
                print('mode: ' + str(mode) + ' not recognized')
                exit()

    def initialize(self):

        refresh_token_path = os.path.join(os.path.expanduser('~'), '.galileo')
        if os.path.exists(refresh_token_path):
            access_token, refresh_token, expires_in = self.refresh_token_file_flow(refresh_token_path)
        else:
            access_token, refresh_token, expires_in = self.device_flow()

        return access_token, refresh_token, expires_in

    def device_flow(self):
        user_url, user_code, device_code, interval, user_url_complete = self._request_device_authorization()

        # Try to open a window to the auth0 audience
        bowser_available = webbrowser.open(user_url_complete)

        if bowser_available:
            # Then arrange code confirmation also in the webbrowser
            self.show_user_code(user_code)
        else:
            mystring = "Go to: " + user_url + "\nEnter the code: " + user_code
            print(mystring)

        access_token, refresh_token, expires_in = self._poll_for_tokens(interval, device_code)
        data = self._store_token_info(refresh_token, expires_in)
        return access_token, refresh_token, data["expires_in"]

    def show_user_code(self, user_code):
        html = '<html> <body> <h1> Make sure this code is the same as the one in the other window: </h1> <p style="font-size:25px;">'+ str(user_code) + '</p> <p> You may close this windows after confirmation. </p> </body> </html>'
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
            url = 'file://' + f.name
            f.write(html)
        webbrowser.open(url, new=1)

    def refresh_token_file_flow(self, refresh_token_file):
        if not os.path.exists(refresh_token_file):
            print('No refresh token file')

        with open(refresh_token_file, 'r') as fd:
            refresh_token = fd.read()

        refresh_json = json.loads(refresh_token)
        refresh_json["expires_in"] = datetime.strptime(refresh_json["expires_in"], "%Y-%m-%d %H:%M:%S.%f")
        access_token = self._get_new_access_token(refresh_json["refresh_token"])
        return access_token, refresh_json["refresh_token"], refresh_json["expires_in"]

    def datetime_converter(self, o):
        if isinstance(o, datetime):
            return o.__str__()

    def _store_token_info(self, refresh_token, expires_in):
        refresh_token_path = os.path.join(os.path.expanduser('~'), '.galileo')
        tmp = None
        data = {
            "refresh_token": refresh_token,
            "expires_in": datetime.now() + timedelta(0, expires_in)
        }

        try:
            tmp = open(refresh_token_path, 'w')
            tmp.write(json.dumps(data, default=self.datetime_converter))
        finally:
            if tmp:
                tmp.close()

        return data

    def _request_device_authorization(self):
        r = requests.post(
            '{domain}/oauth/device/code'.format(domain=self.domain),
            headers=self.headers_default,
            data=urllib.parse.urlencode({
                'client_id': self.client_id,
                'audience': self.audience,
                'scope': 'email profile openid offline_access'
            }, doseq=True),
        )
        r = r.json()
        user_url = r['verification_uri']
        user_code = r['user_code']
        device_code = r['device_code']
        interval = r['interval']
        user_url_complete = r['verification_uri_complete']
        return user_url, user_code, device_code, interval, user_url_complete

    def _poll_for_tokens(self, interval, device_code):
        interval = interval * 2
        url_str = urllib.parse.urlencode({
            'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
            'device_code': device_code,
            'client_id': self.client_id
        }, doseq=True)

        while True:
            try:
                r = requests.post(
                    '{domain}/oauth/token'.format(domain=self.domain),
                    headers=self.headers_default,
                    data=urllib.parse.urlencode({
                        'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
                        'device_code': device_code,
                        'client_id': self.client_id
                    }, doseq=True)
                )
            except urllib.error.URLError as e:
                if e.code == 429:
                    interval = interval * 2
                continue

            if r.status_code == 200:
                break

            time.sleep(interval)

        r = r.json()

        return r["access_token"], r["refresh_token"], r["expires_in"]

    def _get_new_access_token(self, refresh_token):
        response = requests.post(
            '{domain}/oauth/token'.format(domain=self.domain),
            headers=self.headers_default,
            data=urllib.parse.urlencode({
                'client_id': self.client_id,
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
            }, doseq=True)
        )
        response.raise_for_status()
        r = response.json()
        self._store_token_info(refresh_token, r["expires_in"])
        return r['access_token']
