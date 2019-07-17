from config import logger_setup, PRIVAT_API_XML
from model import ExRate, peewee_datetime
import requests

log = logger_setup("PrivatApiXml")

def update_xrate(from_currency, to_currency):
    log.info("Started update for: %s => %s" % (from_currency, to_currency))
    xrate = ExRate.select().where(ExRate.from_currency == from_currency, ExRate.to_currency == to_currency).first()
    log.debug("xrate before: %s", xrate)
    xrate.updated = peewee_datetime.datetime.now()
    xrate.rate = get_privat_rate(from_currency)
    xrate.save()
    log.debug("xrate after: %s", xrate)
    log.info("Finished update for %s => %s" % (from_currency, to_currency))

def get_privat_rate(from_currency):
    response = requests.get(PRIVAT_API_XML)
    response_text = response.text
    log.debug("Privat response: %s", response_text)
    rate = get_rate_xml(response_text)
    return rate

def get_rate_xml(response_text):
    from xml.etree import ElementTree as ET
    tree = ET.fromstring(response_text)
    for item in tree:
        for e in item:
            if e.attrib["ccy"] == 'EUR':
                return(float(e.attrib['sale']))
    raise ValueError("Invalid PrivatBank response: 'EUR' not found")
        