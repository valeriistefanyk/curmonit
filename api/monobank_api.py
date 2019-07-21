import requests
from config import MONOBANK_API_JSON
from api import _Api

class Api(_Api):
    def __init__(self):
            return super().__init__("MonobankApi")    
    def _update_concrete_rate(self, xrate):
            rate = self._get_mono_rate(xrate.from_currency, xrate.to_currency)
            return rate    
    
    def _get_mono_rate(self, from_currency, to_currency):
        response = self._send_request(url = MONOBANK_API_JSON, method = "get")
        response_json = response.json()
        self.log.debug("Monobank response: %s", response_json)
        rate = self._find_rate(response_json, from_currency, to_currency)
        return rate    

    def _find_rate(self, response_json, from_currency, to_currency = 980):
        mono_aliases_map ={
            840: "USD",
            643: "RUB",
            978: "EUR",
            980: "UAH"
        }
        if from_currency not in mono_aliases_map:
                raise ValueError(f"Invalid from_currency: {from_currency}")

        from_currency_alias = mono_aliases_map[from_currency]
        to_currency_alias = mono_aliases_map[to_currency]
        for item in response_json:
            if item['currencyCodeA'] == from_currency and item['currencyCodeB'] == to_currency:
                    return(item['rateSell'])
        raise ValueError(f"Invalid Monobank response: '{from_currency_alias}' not found")
            