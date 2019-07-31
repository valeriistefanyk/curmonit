import unittest, json
from unittest.mock import patch
import models, requests
from config import MONOBANK_API_JSON, PRIVAT_API_JSON, PRIVAT_API_XML, CRYPTONATOR_BTC_TO_UAH, CODE_DICT
import api
import xmltodict
import xml.etree.ElementTree as ET


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
        #models.init_db()
        pass
    

    @unittest.skip("skip")
    def test_privat_usd(self):
        
        xrate = models.ExRate.get(from_currency=CODE_DICT["USD"], to_currency = CODE_DICT["UAH"])
        update_before = xrate.updated
        self.assertEqual(xrate.rate, 1.0)
        
        api.update_xrate(840, 980)
        
        xrate = models.ExRate.get(from_currency=CODE_DICT["USD"], to_currency = CODE_DICT["UAH"])
        update_after = xrate.updated
        
        self.assertGreater(xrate.rate, 25)
        self.assertGreater(update_after, update_before)
        
        self.assertApiLog(PRIVAT_API_JSON, '{"ccy":"USD","base_ccy":"UAH",')
    
    @unittest.skip("skip")
    def test_privat_currency_error(self):
        
        xrate = models.ExRate.get(id = 1)
        self.assertEqual(xrate.rate, 1.0)
        self.assertRaises(ValueError, api.update_xrate, 978, 980)
    
    @unittest.skip("skip")
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
    
    @unittest.skip("skip")
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
    
    @unittest.skip("skip")
    def test_privat_xml(self):
        xrate = models.ExRate.get(from_currency=CODE_DICT["EUR"], to_currency = CODE_DICT["UAH"])
        update_before = xrate.updated
        self.assertEqual(xrate.rate, 1.0)
        api.update_xrate(CODE_DICT["EUR"], CODE_DICT["UAH"])
        xrate = models.ExRate.get(from_currency=CODE_DICT["EUR"], to_currency = CODE_DICT["UAH"])
        update_after = xrate.updated
        self.assertGreater(xrate.rate, 27)
        self.assertGreater(update_after, update_before)
        self.assertApiLog(PRIVAT_API_XML, '<exchangerate ccy="EUR" base_ccy="UAH"')
    
    @unittest.skip("skip")
    def test_mono_rub(self):
        xrate = models.ExRate.get(from_currency=CODE_DICT["RUB"], to_currency = CODE_DICT["UAH"])
        update_before = xrate.updated
        self.assertEqual(xrate.rate, 1.0)
        api.update_xrate(CODE_DICT["RUB"], CODE_DICT["UAH"])
        xrate = models.ExRate.get(from_currency=CODE_DICT["RUB"], to_currency = CODE_DICT["UAH"])
        update_after = xrate.updated
        self.assertGreater(xrate.rate, 0.3)
        self.assertGreater(update_after, update_before)
        self.assertApiLog(MONOBANK_API_JSON, '{"currencyCodeA":643,"currencyCodeB":980,')

    @unittest.skip("skip")
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
 
    @unittest.skip("skip")
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

    @unittest.skip("skip")
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

    def assertApiLog(self, url, text):
        api_log = models.ApiLog.select().order_by(models.ApiLog.created.desc()).first()
        self.assertIsNotNone(api_log)
        self.assertEqual(api_log.request_url, url)
        self.assertIsNotNone(api_log.response_text)
        self.assertIn(text, api_log.response_text)
    


    ### TEST CUTMONIT API ###
    @unittest.skip("skip")
    def test_xml_api(self):
        r = requests.get("http://127.0.0.1:5001/api/xrates/xml")
        self.assertIn("<xrates>", r.text)
        xml_rates = xmltodict.parse(r.text)
        self.assertIn("xrates", xml_rates)
        self.assertIsInstance(xml_rates["xrates"]["xrate"], list)
        self.assertEqual(len(xml_rates["xrates"]["xrate"]), 6)
    
    @unittest.skip("skip")
    def test_json_api(self):
        r = requests.get("http://127.0.0.1:5001/api/xrates/json")
        json_rates = r.json()
        self.assertIsInstance(json_rates, list)
        self.assertEqual(len(json_rates), 6)
        for rate in json_rates:
            self.assertIn("from", rate)
            self.assertIn("to", rate)
            self.assertIn("rate", rate)

    @unittest.skip("skip")
    def test_json_api_uah(self):
        r = requests.get("http://127.0.0.1:5001/api/xrates/json?to_currency=980")
        json_rates = r.json()
        self.assertIsInstance(json_rates, list)
        self.assertEqual(len(json_rates), 4)


    ### TEST UPDATE RATE ###

    def test_html_xrates(self):
        r = requests.get("http://127.0.0.1:5001/xrates")
        self.assertTrue(r.ok)
        self.assertIn('<table border="1">', r.text)
        root = ET.fromstring(r.text)
        body = root.find("body")
        self.assertIsNotNone(body)
        table = body.find("table")
        self.assertIsNotNone(table)
        rows = table.findall("tr")
        self.assertEqual(len(rows), 6)

if __name__ == "__main__":
    unittest.main()