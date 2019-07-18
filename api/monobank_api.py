import requests
from config import MONOBANK_API_JSON
from api import _Api

class MonobankApi(_Api):
        def __init__(self):
                return super().__init__("MonobankApi")

        def _update_concrete_rate(self, xrate):
                rub_rate = self._get_mono_rate(xrate.from_currency)
                return rub_rate

        def _get_mono_rate(self, from_currency):
            response = self._send_request(url = MONOBANK_API_JSON, method = "get")
            response_json = response.json()
            self.log.debug("Monobank response: %s", response_json)
            rub_rate = self._find_rub_rate(response_json)
            return rub_rate

        def _find_rub_rate(self, response_json):
            for item in response_json:
                if item['currencyCodeA'] == 643:
                    return(item['rateSell'])
            raise ValueError("Invalid Monobank response: 'RUB' not found")