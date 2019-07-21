import requests
from api import _Api
from config import CRYPTONATOR_BTC_TO_UAH

class Api(_Api):
    def __init__(self):
                return super().__init__("CryptonatorApiJson")

    def _update_concrete_rate(self, xrate):
        rate = self._get_cryptonator_rate(xrate.from_currency, xrate.to_currency)
        return rate
    def _get_cryptonator_rate(self, from_currency, to_currency):
        response = self._send_request(url = CRYPTONATOR_BTC_TO_UAH, method = "get")
        response_json = response.json()
        self.log.debug("Cryptonator response: %s", response_json)
        rate = self._find_rate(response_json, from_currency, to_currency)
        return rate

    def _find_rate(self, response_json, from_currency, to_currency):
        cryptonator_aliases_map = {
            980: "UAH",
            1000: "BTC"
        }
        if from_currency not in cryptonator_aliases_map:
            raise ValueError(f"Invalid from_currency: {from_currency}")
        if to_currency not in cryptonator_aliases_map:
            raise ValueError(f"Invalid to_currency: {to_currency}")
        
        from_currency_alias = cryptonator_aliases_map[from_currency]
        to_currency_alias = cryptonator_aliases_map[to_currency]

        ticker = response_json['ticker']
        if ticker['base'] == from_currency_alias and ticker['target'] == to_currency_alias:
            return float(ticker["price"])
            
        raise ValueError(f"Invalid cryptonator response: {from_currency_alias} not found")