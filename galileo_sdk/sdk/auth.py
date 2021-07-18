from galileo_sdk.compat import requests, urlencode, URLError
from datetime import datetime, timedelta
import os, urllib, json, webbrowser, time, tempfile


# wrapper class for Galileo sdk authentication. It automatically handles authentication for the user via the default webbrowser
class AuthSdk:
    """Helper class for user authentication."""
    def __init__(self,
                 client_id="oDmH6Nf4DN3oILcNk7cQqBchXUfv7fpD",
                 audience=""):
        """
        Constructor for AuthSdk class.

        :param client_id: string: Optional argument for tracking which integration is calling the sdk.
        :param mode: string: Optional argument, can be prod (default) or dev.
        :param audience: string: Optional argument
        :return: AuthSdk
        
        Example:
            >>> from galileo_sdk import GalileoSdk, AuthSdk
            >>> myauth = AuthSdk()
            >>> access_token, refresh_token, expiry_time = myauth.initialize()
            >>> galileo = GalileoSdk(auth_token=access_token, refresh_token=refresh_token)
        
        """
        self.domain = "https://galileoapp.auth0.com"
        self.headers_default = {
            "content-type": "application/x-www-form-urlencoded"
        }
        self.client_id = client_id

        # if a custom audience is supplied, use it
        if audience:
            self.audience = audience
        else:
            self.audience = "https://api.galileoapp.io"

    def initialize(self,
                   refresh_token_path=os.path.join(os.path.expanduser("~"),
                                                   ".galileo")):
        """
        Automatically authenticate the user either through a webbrowser or auth-link printed to the terminal.

        :param refresh_token_path: string: An optional file path for where to store auth token information. If you don not want authentication info to be stored, pass an empty string, i.e. refresh_token_path=''. The default location is in you home directory in a file named .galileo.
        :return: access_token, refresh_token, expiration
        
        Example:
            >>> from galileo_sdk import GalileoSdk, AuthSdk
            >>> myauth = AuthSdk()
            >>> access_token, refresh_token, expiry_time = myauth.initialize()
            >>> galileo = GalileoSdk(auth_token=access_token, refresh_token=refresh_token)
        
        """

        if os.path.exists(refresh_token_path):
            access_token, refresh_token, expires_in = self.refresh_token_file_flow(
                refresh_token_path)
        else:
            access_token, refresh_token, expires_in = self.device_flow(
                refresh_token_path)

        return access_token, refresh_token, expires_in

    def device_flow(self, refresh_token_path=""):
        """
        Attempts to bring up a webbrowser for the user to authenticate. Otherwise, it will print a URL and access code to stdout.

        :param refresh_token_path: string: An optional file path for where to store auth token information. If you do not provide a file path, the programmer is responsible for handling persistence.
        :return: access_token, refresh_token, expiration
        """
        (
            user_url,
            user_code,
            device_code,
            interval,
            user_url_complete,
        ) = self._request_device_authorization()

        # Try to open a window to the auth0 audience
        bowser_available = webbrowser.open(user_url_complete)

        if bowser_available:
            # Then arrange code confirmation also in the webbrowser
            self.show_user_code(user_code)
        else:
            mystring = "Go to: " + user_url + "\nEnter the code: " + user_code
            print(mystring)

        access_token, refresh_token, expires_in = self._poll_for_tokens(
            interval, device_code)
        data = self._store_token_info(refresh_token, expires_in,
                                      refresh_token_path)
        return access_token, refresh_token, data["expires_in"]

    def show_user_code(self, user_code):
        html = ("""<!DOCTYPE html> 
<html> 
<head>
        <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    
    <meta name="robots" content="noindex, nofollow">
    
    
    <link rel="stylesheet" href="https://cdn.auth0.com/ulp/react-components/1.14.1/css/main.cdn.min.css">
    <style id="custom-styles-container">
      

body {
  background: #354962;
  font-family: ulp-font, -apple-system, BlinkMacSystemFont, Roboto, Helvetica, sans-serif;
}
.main-wrapper {
  background: #354962;
}
.ulp-alert.danger {
  background: #D00E17;
}
.ulp-alert.success {
  background: #0A8852;
}
@supports (mask-image: url('/static/img/branding-generic/copy-icon.svg')) {
  @supports not (-ms-ime-align: auto) {
    .input-container.error::before {
      background-color: #D00E17;
    }
  }
}
.input.ulp-input-error {
  border-color: #D00E17;
}
.error-cloud {
  background-color: #D00E17;
}
.error-fatal {
  background-color: #D00E17;
}
    </style>
    
    <title>Connect to Galileo SDK/CLI</title>
  </head> 

<body>
<main class="ulp-outer device-code-confirmation">
  <section class="ulp-box   no-badge">
    <div class="ulp-box-inner _prompt-box">
      <div class="ulp-main">
        <header class="ulp-header _prompt-header">
          <img class="header-logo _header-logo" id="prompt-logo-center" src="https://galileoapp.io/wp-content/uploads/2019/02/galileo-icon-03.png" alt="Device Confirmation">
        
          <h1 class="header-title _header-title">Device Confirmation</h1>
        
          <div class="header-description _header-description">
            <p class="text-simple _text  ">Please confirm this code in the other tab:</p>
          </div>
          <div class="header-description _header-description">
            <p class="text-simple _text  " style="font-size:25px;">""" +
                str(user_code) + """</p>
          </div>
        </header>
      
      </div>
    </div>
</body>
</html>
  """)
        with tempfile.NamedTemporaryFile("w", delete=False,
                                         suffix=".html") as f:
            url = "file://" + f.name
            f.write(html)
        webbrowser.open(url, new=1)

    def refresh_token_file_flow(self, refresh_token_file):
        """
        Refreshes access token if given the location of a refresh token file.

        :param refresh_token_file: string: File path for where auth token information is stored.
        :return: access_token, refresh_token, expiration
        """
        if not os.path.exists(refresh_token_file):
            print("No refresh token file")

        with open(refresh_token_file, "r") as fd:
            refresh_token = fd.read()

        refresh_json = json.loads(refresh_token)
        refresh_json["expires_in"] = datetime.strptime(
            refresh_json["expires_in"], "%Y-%m-%d %H:%M:%S.%f")
        access_token = self._get_new_access_token(
            refresh_json["refresh_token"], refresh_token_file)
        return access_token, refresh_json["refresh_token"], refresh_json[
            "expires_in"]

    def refresh_token_flow(self, refresh_token, expires_in):
        """
        Refreshes access token if given a refresh token.

        :param refresh_token: string: String object representing the token.
        :param expires_in: string: String object representing the expiry date of the refresh token.
        :return: access_token, refresh_token, expiration
        """
        access_token = self._get_new_access_token(refresh_token, "")
        return access_token, refresh_token, expires_in

    def datetime_converter(self, o):
        """
        :param o: object: Object to convert to datetime.

        :return: datetime: str: String representation of the object.
        """
        if isinstance(o, datetime):
            return o.__str__()

    def _store_token_info(self, refresh_token, expires_in, refresh_token_path):
        """
        :param refresh_token: string: refresh token. 
        :param expires_in: string: expiration date of the refresh token.
        :param refresh_token_path: string: file path to store the refresh token.

        :return: token_info: dict: Dictionary containing the refresh token, expiration date
        """

        tmp = None
        data = {
            "refresh_token": refresh_token,
            "expires_in": datetime.now() + timedelta(0, expires_in),
        }

        if len(refresh_token_path) > 0:
            try:
                tmp = open(refresh_token_path, "w")
                tmp.write(json.dumps(data, default=self.datetime_converter))
            finally:
                if tmp:
                    tmp.close()

        return data

    def _request_device_authorization(self):
        """
        :return: Tuple containing the user_url, user_code, device_code, interval, and complete_url.
        """
        r = requests.post(
            "{domain}/oauth/device/code".format(domain=self.domain),
            headers=self.headers_default,
            data=urlencode(
                {
                    "client_id": self.client_id,
                    "audience": self.audience,
                    "scope": "email profile openid offline_access",
                },
                doseq=True,
            ),
        )
        r = r.json()
        user_url = r["verification_uri"]
        user_code = r["user_code"]
        device_code = r["device_code"]
        interval = r["interval"]
        user_url_complete = r["verification_uri_complete"]
        return user_url, user_code, device_code, interval, user_url_complete

    def _poll_for_tokens(self, interval, device_code):
        """
        :param interval: string: time in seconds between polling for tokens.
        :param device_code: string: device code.
        :return: Tuple containing the access_token, refresh_token, and expiration.
        """
        interval = interval * 2
        url_str = urlencode(
            {
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                "device_code": device_code,
                "client_id": self.client_id,
            },
            doseq=True,
        )

        while True:
            try:
                r = requests.post(
                    "{domain}/oauth/token".format(domain=self.domain),
                    headers=self.headers_default,
                    data=urlencode(
                        {
                            "grant_type":
                            "urn:ietf:params:oauth:grant-type:device_code",
                            "device_code": device_code,
                            "client_id": self.client_id,
                        },
                        doseq=True,
                    ),
                )
            except Exception as e:
                if hasattr(e, "code") and e.code == 429:
                    interval = interval * 2
                continue

            if r.status_code == 200:
                break

            time.sleep(interval)

        r = r.json()

        return r["access_token"], r["refresh_token"], r["expires_in"]

    def _get_new_access_token(self, refresh_token, refresh_token_file):
        """
        :param refresh_token: string: refresh token.
        :param refresh_token_file: string: file path for where the refresh token is stored.
        :return: access_token: string: access token.
        """
        response = requests.post(
            "{domain}/oauth/token".format(domain=self.domain),
            headers=self.headers_default,
            data=urlencode(
                {
                    "client_id": self.client_id,
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                },
                doseq=True,
            ),
        )
        response.raise_for_status()
        r = response.json()
        self._store_token_info(refresh_token, r["expires_in"],
                               refresh_token_file)
        return r["access_token"]
