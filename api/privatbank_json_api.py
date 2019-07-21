import requests
from config import PRIVAT_API_JSON
from api import _Api

class Api(_Api):
        def __init__(self):
                return super().__init__("PrivatJsonApi")

        def _update_concrete_rate(self, xrate):
            rate = self._get_privat_rate(xrate.from_currency)
            return rate

        def _get_privat_rate(self, from_currency):
            response = self._send_request(url = PRIVAT_API_JSON, method = "get")
            response_json = response.json()
            self.log.debug("Privat response: %s", response_json)
            rate = self._find_rate(response_json, from_currency)
            return rate

        def _find_rate(self, response_json, from_currency):
            privat_aliases_map = {
                840: "USD",
                1000: "BTC"
            }
            if from_currency not in privat_aliases_map:
                raise ValueError(f"Invalid from_currency: {from_currency}")
            
            currency_alias = privat_aliases_map[from_currency]
            for e in response_json:
                if e['ccy'] == currency_alias:
                    return float(e['sale'])
            
            raise ValueError(f"Invalid Privat response: {currency_alias} not found")
                
                