import requests
from model import ExRate, peewee_datetime
from config import PRIVAT_API_JSON, logger_setup

log = logger_setup("PrivatApiJson")

def update_xrate(from_currency, to_currency):
    log.info("Started update for: %s => %s" % (from_currency, to_currency))
    xrate = ExRate.select().where(ExRate.from_currency == from_currency, ExRate.to_currency == to_currency).first()
    log.debug("rate before: %s", xrate)
    xrate.rate = get_privat_rate(from_currency)
    xrate.updated = peewee_datetime.datetime.now()
    xrate.save()
    log.debug("rate after: %s", xrate)
    log.info("Finished update for: %s => %s" % (from_currency, to_currency))

def get_privat_rate(from_currency):
    response = requests.get(PRIVAT_API_JSON)
    response_json = response.json()
    log.debug("Privat response: %s", response_json)
    usd_rate = find_usd_rate(response_json)
    return usd_rate

def find_usd_rate(response_json):
    for e in response_json:
        if e['ccy'] == 'USD':
            return float(e['sale'])
    raise ValueError("Invalid Privat response: 'USD' not found")