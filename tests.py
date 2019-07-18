import unittest, json
from unittest.mock import patch
import models, requests
from config import MONOBANK_API_JSON, PRIVAT_API_JSON, PRIVAT_API_XML
import api.test_api as test_api
import api.privatbank_json_api as privatbank_json_api
import api.monobank_api as monobank_api
import api.privatbank_xml_api as privatbank_xml_api
import api
from config import TEST_CUR

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

    def test_main(self):
        xrate = models.ExRate.get(id = 1)
        self.assertEqual(xrate.rate, TEST_CUR["USD"]['rate'])
        test_api.update_xrate(TEST_CUR["USD"]['from_currency'], TEST_CUR["USD"]['to_currency'])
        xrate = models.ExRate.get(id = 1)
        self.assertEqual(xrate.rate, 1.01)

    def test_privat_json(self):
        xrate = models.ExRate.get(id = 1)
        update_before = xrate.updated
        self.assertEqual(xrate.rate, TEST_CUR["USD"]['rate'])
        privatbank_json_api.PrivatJsonApi().update_xrate(TEST_CUR["USD"]['from_currency'], TEST_CUR["USD"]['to_currency'])
        xrate = models.ExRate.get(id = 1)
        update_after = xrate.updated
        self.assertGreater(xrate.rate, 25)
        self.assertGreater(update_after, update_before)
        self.assertApiLog(PRIVAT_API_JSON, '{"ccy":"USD","base_ccy":"UAH",')

    def test_privat_xml(self):
        xrate = models.ExRate.get(id = 2)
        update_before = xrate.updated
        self.assertEqual(xrate.rate, TEST_CUR["EUR"]['rate'])
        privatbank_xml_api.PrivatXmlApi().update_xrate(TEST_CUR["EUR"]["from_currency"], TEST_CUR["EUR"]["to_currency"])
        xrate = models.ExRate.get(id = 2)
        update_after = xrate.updated
        self.assertGreater(xrate.rate, 27)
        self.assertGreater(update_after, update_before)
        self.assertApiLog(PRIVAT_API_XML, '<exchangerate ccy="EUR" base_ccy="UAH"')

    def test_mono(self):
        xrate = models.ExRate.get(id = 3)
        update_before = xrate.updated
        self.assertEqual(xrate.rate, TEST_CUR["RUB"]["rate"])
        monobank_api.MonobankApi().update_xrate(TEST_CUR["RUB"]["from_currency"], TEST_CUR["RUB"]["to_currency"])
        xrate = models.ExRate.get(id = 3)
        update_after = xrate.updated
        self.assertGreater(xrate.rate, 0.3)
        self.assertGreater(update_after, update_before)
        self.assertApiLog(MONOBANK_API_JSON, '{"currencyCodeA":643,"currencyCodeB":980,')

    @patch('api._Api._send', new = get_privat_response)
    def test_pritvat_mock(self):
        xrate = models.ExRate.get(id = 1)
        update_before = xrate.updated
        self.assertEqual(xrate.rate, TEST_CUR["USD"]['rate'])
        privatbank_json_api.PrivatJsonApi().update_xrate(TEST_CUR["USD"]['from_currency'], TEST_CUR["USD"]['to_currency'])
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
        api.HTTP_TIMEOUT = 0.001
        xrate = models.ExRate.get(id = 1)
        updated_before = xrate.updated
        self.assertEqual(xrate.rate, 1.0)
        self.assertRaises(requests.RequestException, privatbank_json_api.PrivatJsonApi().update_xrate, TEST_CUR["USD"]['from_currency'], TEST_CUR["USD"]['to_currency'])

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