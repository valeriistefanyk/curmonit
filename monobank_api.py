import requests
from config import MONOBANK_API_JSON, logger_setup
from model import ExRate, peewee_datetime

log = logger_setup("MonobankApi")

def update_xrate(from_currency, to_currency):
    log.info("Started update rate for %s => %s" % (from_currency, to_currency))
    xrate = ExRate.select().where(ExRate.from_currency == from_currency, ExRate.to_currency == to_currency).first()
    log.debug("rate before: %s", xrate.rate)
    xrate.updated = peewee_datetime.datetime.now()
    xrate.rate = get_mono_rate(from_currency)
    xrate.save()
    log.debug("rate after: %s", xrate.rate)
    log.info("Finished update rate for %s => %s" % (from_currency, to_currency))

def get_mono_rate(from_currency):
    response = requests.get(MONOBANK_API_JSON)
    response_json = response.json()
    log.debug("Monobank response: %s", response_json)
    rub_rate = find_rub_rate(response_json)
    return rub_rate

def find_rub_rate(response_json):
    for item in response_json:
        if item['currencyCodeA'] == 643:
            return(item['rateSell'])
    raise ValueError("Invalid Monobank response: 'RUB' not found")