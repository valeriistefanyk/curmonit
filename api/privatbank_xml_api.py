from config import PRIVAT_API_XML
import requests
from api import _Api

class PrivatXmlApi(_Api):
    def __init__(self):
        return super().__init__("PrivatXmlApi")

    def _update_concrete_rate(self, xrate):
        eur_rate = self._get_eur_rate(xrate.from_currency)
        return eur_rate

    def _get_eur_rate(self, from_currency):
        response = self._send_request(url = PRIVAT_API_XML, method = "get")
        response_text = response.text
        self.log.debug("Privat response: %s", response_text)
        rate = self._find_rate_xml(response_text)
        return rate

    def _find_rate_xml(self, response_text):
        from xml.etree import ElementTree as ET
        tree = ET.fromstring(response_text)
        for item in tree:
            for e in item:
                if e.attrib["ccy"] == 'EUR':
                    return(float(e.attrib['sale']))
        raise ValueError("Invalid PrivatBank response: 'EUR' not found")
