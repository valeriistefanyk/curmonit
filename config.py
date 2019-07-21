import logging

# название базы данных
DB_NAME = "curmonit.db"

# web api, get string
PRIVAT_API_JSON = "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11"
PRIVAT_API_XML = "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=11"
MONOBANK_API_JSON = "https://api.monobank.ua/bank/currency"
CRYPTONATOR_BTC_TO_UAH = "https://api.cryptonator.com/api/ticker/btc-uah"

# для тестов
CODE_DICT= {
    "USD": 840,
    "EUR": 978,
    "UAH": 980,
    "RUB": 643,
    "BTC": 1000
}

# настройки для логгирования
LOGGER_CONFIG = {
    "level": logging.DEBUG,
    "file": "app.log",
    "formatter": logging.Formatter("%(asctime)s [%(levelname)s]\t - \t%(name)s:%(message)s")
}

def logger_setup(logger_name):
    log = logging.getLogger(logger_name)
    fh = logging.FileHandler(LOGGER_CONFIG["file"])
    fh.setLevel(LOGGER_CONFIG["level"])
    fh.setFormatter(LOGGER_CONFIG["formatter"])
    log.addHandler(fh)
    log.setLevel(LOGGER_CONFIG["level"])
    return log

HTTP_TIMEOUT = 15