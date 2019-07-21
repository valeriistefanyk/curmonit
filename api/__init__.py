import traceback
import requests
import importlib
from models import ExRate, peewee_datetime, ApiLog, ErrorLog
from config import HTTP_TIMEOUT, LOGGER_CONFIG, logging


fh = logging.FileHandler(LOGGER_CONFIG["file"])
fh.setLevel(LOGGER_CONFIG["level"])
fh.setFormatter(LOGGER_CONFIG["formatter"])


def update_xrate(from_currency, to_currency):
    xrate = ExRate.select().where(ExRate.from_currency == from_currency, 
                                ExRate.to_currency == to_currency).first()
    module = importlib.import_module(f"api.{xrate.module}")
    module.Api().update_xrate(xrate)


class _Api:
    def __init__(self, logger_name):
        self.log = logging.getLogger(logger_name)
        self.log.addHandler(fh)
        self.log.setLevel(LOGGER_CONFIG["level"])
    
    def update_xrate(self, xrate):
        self.log.info("Started update rate for %s => %s" % (xrate.from_currency, xrate.to_currency))
        self.log.debug("rate before: %s", xrate.rate)
        xrate.updated = peewee_datetime.datetime.now()
        xrate.rate = self._update_concrete_rate(xrate)
        xrate.save()
        self.log.debug("rate after: %s", xrate.rate)
        self.log.info("Finished update rate for %s => %s" % (xrate.from_currency, xrate.to_currency))

    def _update_concrete_rate(self, xrate):
        raise NotImplementedError("_update_concrete_rate")

    def _send_request(self, url, method, data = None, headers = None):
        log = ApiLog(request_url = url, request_data = data, request_method = method, request_headers = headers)
        try:
            response = self._send(method = method, url = url, headers = headers, data = data)
            log.response_text = response.text
            return response
        except Exception as ex:
            self.log.exception("Error during request sending")
            log.error = str(ex)
            ErrorLog.create(request_data = data, request_url = url, request_method = method, 
                            error = str(ex), traceback = traceback.format_exc(chain=False))
            raise
        finally:
            log.finished = peewee_datetime.datetime.now()
            log.save()

    def _send(self, url, method, data = None, headers = None):
        return requests.request(method = method, url = url, headers = headers, data = data, timeout = HTTP_TIMEOUT)