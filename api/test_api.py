from models import ExRate
from config import logger_setup

log = logger_setup("TestApi")

def update_xrate(from_currency, to_currency):
    log.info("Started update for: %s => %s" % (from_currency, to_currency))
    xrate = ExRate.select().where(ExRate.from_currency == from_currency, ExRate.to_currency == to_currency).first()
    log.debug("rate before: %s", xrate)
    xrate.rate += 0.01
    xrate.save()
    xrate = ExRate.select().where(ExRate.from_currency == from_currency, ExRate.to_currency == to_currency).first()
    log.debug("xrate after: %s", xrate)
    log.info("Finished update for: %s => %s" % (from_currency, to_currency))

