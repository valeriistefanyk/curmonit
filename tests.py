import unittest
import model, test_api, privatbank_json_api, privatbank_xml_api, monobank_api
from config import TEST_CUR, TEST_CUR


class Test(unittest.TestCase):
    def setUp(self):
        model.init_db()

    def test_main(self):
        xrate = model.ExRate.get(id = 1)
        # сравнить xrate.id = 1 со значением 1.0
        self.assertEqual(xrate.rate, TEST_CUR["USD"]['rate'])
        test_api.update_xrates(TEST_CUR["USD"]['from_currency'], TEST_CUR["USD"]['to_currency'])
        xrate = model.ExRate.get(id = 1)
        # сравнить xrate.id = 1 со значением 1.01 (update_xrates увеличивает значение rate на 0.01)
        self.assertEqual(xrate.rate, 1.01)

    def test_privat_json(self):
        xrate = model.ExRate.get(id = 1)
        update_before = xrate.updated
        self.assertEqual(xrate.rate, TEST_CUR["USD"]['rate'])
        privatbank_json_api.update_xrate(TEST_CUR["USD"]['from_currency'], TEST_CUR["USD"]['to_currency'])
        xrate = model.ExRate.get(id = 1)
        update_after = xrate.updated
        self.assertGreater(xrate.rate, 25)
        self.assertGreater(update_after, update_before)

    def test_privat_xml(self):
        xrate = model.ExRate.get(id = 2)
        update_before = xrate.updated
        self.assertEqual(xrate.rate, TEST_CUR["EUR"]['rate'])
        privatbank_xml_api.update_xrate(TEST_CUR["EUR"]["from_currency"], TEST_CUR["EUR"]["to_currency"])
        xrate = model.ExRate.get(id = 2)
        update_after = xrate.updated
        self.assertGreater(xrate.rate, 27)
        self.assertGreater(update_after, update_before)

    def test_mono(self):
        xrate = model.ExRate.get(id = 3)
        update_before = xrate.updated
        self.assertEqual(xrate.rate, TEST_CUR["RUB"]["rate"])
        monobank_api.update_xrate(TEST_CUR["RUB"]["from_currency"], TEST_CUR["RUB"]["to_currency"])
        xrate = model.ExRate.get(id = 3)
        update_after = xrate.updated
        self.assertGreater(xrate.rate, 0.3)
        self.assertGreater(update_after, update_before)

if __name__ == "__main__":
    unittest.main()