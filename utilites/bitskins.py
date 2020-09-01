import requests
import pyotp


class Bitskins:
    def __init__(self, apikey, secretkey):
        self.apikey = apikey
        self.secretkey = secretkey

    def get_request(self, url, params_vars=None):
        auth_token = pyotp.TOTP(self.secretkey)
        params_req = {"api_key": self.apikey, "code": auth_token.now()}

        if params_vars:
            params = {**params_req, **params_vars}
        else:
            params = params_req

        r = requests.get("https://bitskins.com/api/v1/" + url, params=params)
        return r.json()
