import unittest, json
from unittest.mock import patch
import models, requests
from config import MONOBANK_API_JSON, PRIVAT_API_JSON, PRIVAT_API_XML, CRYPTONATOR_BTC_TO_UAH, CODE_DICT
import api

def get_privat_response(*args, **kwds):
    print("get_private_response")
    class Response:
        def __init__(self, response):
            self.text = json.dumps(response)
        
        def json(self):
            return json.loads(self.text)
    return Response([{"ccy": "USD", "base_ccy": "UAH", "sale": "30.0"}])

class Test(unittest.TestCase):
    def setUp(self):
        models.init_db()

    def test_privat_usd(self):
        
        xrate = models.ExRate.get(id = 1)
        update_before = xrate.updated
        self.assertEqual(xrate.rate, 1.0)
        
        api.update_xrate(840, 980)
        
        xrate = models.ExRate.get(id = 1)
        update_after = xrate.updated
        
        self.assertGreater(xrate.rate, 25)
        self.assertGreater(update_after, update_before)
        
        self.assertApiLog(PRIVAT_API_JSON, '{"ccy":"USD","base_ccy":"UAH",')

    # def test_privat_currency_error(self):
        
    #     xrate = models.ExRate.get(id = 1)
    #     self.assertEqual(xrate.rate, 1.0)
    #     self.assertRaises(ValueError, api.update_xrate, 978, 980)
    

    def test_privat_btc(self):
        xrate = models.ExRate.get(from_currency=CODE_DICT["BTC"], to_currency = CODE_DICT["USD"])
        update_before = xrate.updated
        self.assertEqual(xrate.rate, 1.0)
        api.update_xrate(CODE_DICT["BTC"], CODE_DICT["USD"])
        xrate = models.ExRate.get(from_currency=CODE_DICT["BTC"], to_currency = CODE_DICT["USD"])
        update_after = xrate.updated
        self.assertGreater(xrate.rate, 25)
        self.assertGreater(update_after, update_before)
        self.assertApiLog(PRIVAT_API_JSON, '{"ccy":"USD","base_ccy":"UAH",')

    def test_cryptonator_btc_to_uah(self):
        xrate = models.ExRate.get(from_currency=CODE_DICT["BTC"], to_currency = CODE_DICT["UAH"])
        update_before = xrate.updated
        self.assertEqual(xrate.rate, 1.0)
        api.update_xrate(CODE_DICT["BTC"], CODE_DICT["UAH"])
        xrate = models.ExRate.get(from_currency=CODE_DICT["BTC"], to_currency = CODE_DICT["UAH"])
        update_after = xrate.updated
        self.assertGreater(xrate.rate, 1000)
        self.assertGreater(update_after, update_before)
        self.assertApiLog(CRYPTONATOR_BTC_TO_UAH, '{"base":"BTC","target":"UAH",')

    def test_privat_xml(self):
        xrate = models.ExRate.get(id = 2)
        update_before = xrate.updated
        self.assertEqual(xrate.rate, 1.0)
        api.update_xrate(CODE_DICT["EUR"], CODE_DICT["UAH"])
        xrate = models.ExRate.get(id = 2)
        update_after = xrate.updated
        self.assertGreater(xrate.rate, 27)
        self.assertGreater(update_after, update_before)
        self.assertApiLog(PRIVAT_API_XML, '<exchangerate ccy="EUR" base_ccy="UAH"')

    def test_mono_rub(self):
        xrate = models.ExRate.get(id = 3)
        update_before = xrate.updated
        self.assertEqual(xrate.rate, 1.0)
        api.update_xrate(CODE_DICT["RUB"], CODE_DICT["UAH"])
        xrate = models.ExRate.get(id = 3)
        update_after = xrate.updated
        self.assertGreater(xrate.rate, 0.3)
        self.assertGreater(update_after, update_before)
        self.assertApiLog(MONOBANK_API_JSON, '{"currencyCodeA":643,"currencyCodeB":980,')

    def test_mono_eur_to_usd(self):
        xrate = models.ExRate.get(from_currency=CODE_DICT["EUR"], to_currency = CODE_DICT["USD"])
        update_before = xrate.updated
        self.assertEqual(xrate.rate, 1.0)
        api.update_xrate(978, 840)
        xrate = models.ExRate.get(from_currency=CODE_DICT["EUR"], to_currency = CODE_DICT["USD"])
        update_after = xrate.updated
        self.assertGreater(xrate.rate, 0.0)
        self.assertGreater(update_after, update_before)
        self.assertApiLog(MONOBANK_API_JSON, '{"currencyCodeA":978,"currencyCodeB":840,')

    @patch('api._Api._send', new = get_privat_response)
    def test_pritvat_mock(self):
        xrate = models.ExRate.get(id = 1)
        update_before = xrate.updated
        self.assertEqual(xrate.rate, 1.0)
        api.update_xrate(CODE_DICT["USD"], CODE_DICT["UAH"])
        xrate = models.ExRate.get(id = 1)
        update_after = xrate.updated
        self.assertGreater(xrate.rate, 25)
        self.assertGreater(update_after, update_before)
        self.assertApiLog(PRIVAT_API_JSON, '[{"ccy": "USD", "base_ccy": "UAH", "sale": "30.0"}]')

    def assertApiLog(self, url, text):
        api_log = models.ApiLog.select().order_by(models.ApiLog.created.desc()).first()
        self.assertIsNotNone(api_log)
        self.assertEqual(api_log.request_url, url)
        self.assertIsNotNone(api_log.response_text)
        self.assertIn(text, api_log.response_text)

    def test_api_error(self):
        api.HTTP_TIMEOUT = 0.01
        xrate = models.ExRate.get(id = 1)
        updated_before = xrate.updated
        self.assertEqual(xrate.rate, 1.0)
        self.assertRaises(requests.RequestException, api.update_xrate, CODE_DICT["USD"], CODE_DICT["UAH"])

        xrate = models.ExRate.get(id = 1)
        updated_after = xrate.updated
        self.assertEqual(xrate.rate, 1.0)
        self.assertEqual(updated_after, updated_before)

        api_log = models.ApiLog.select().order_by(models.ApiLog.created.desc()).first()
        self.assertIsNotNone(api_log)
        self.assertEqual(api_log.request_url, PRIVAT_API_JSON)
        self.assertIsNone(api_log.response_text)
        self.assertIsNotNone(api_log.error)

        error_log = models.ErrorLog.select().order_by(models.ErrorLog.created.desc()).first()
        self.assertIsNotNone(error_log)
        self.assertEqual(error_log.request_url, PRIVAT_API_JSON)
        self.assertIsNotNone(error_log.traceback)
        self.assertEqual(api_log.error, error_log.error)
        self.assertIn("Connection to api.privatbank.ua timed out", error_log.error)

        api.HTTP_TIMEOUT = 15


if __name__ == "__main__":
    unittest.main()