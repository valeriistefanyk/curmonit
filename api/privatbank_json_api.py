import requests
from config import PRIVAT_API_JSON
from api import _Api

class PrivatJsonApi(_Api):
        def __init__(self):
                return super().__init__("PrivatJsonApi")

        def _update_concrete_rate(self, xrate):
            usd_rate = self._get_privat_rate(xrate.from_currency)
            return usd_rate

        def _get_privat_rate(self, from_currency):
            response = self._send_request(url = PRIVAT_API_JSON, method = "get")
            response_json = response.json()
            self.log.debug("Privat response: %s", response_json)
            usd_rate = self._find_usd_rate(response_json)
            return usd_rate

        def _find_usd_rate(self, response_json):
            for e in response_json:
                if e['ccy'] == 'USD':
                    return float(e['sale'])
            raise ValueError("Invalid Privat response: 'USD' not found")