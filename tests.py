import unittest
import model, test_api
from config import FOR_TEST_DB

class Test(unittest.TestCase):
    def setUp(self):
        model.init_db()

    def test_main(self):
        xrate = model.ExRate.get(id = 1)
        # сравнить xrate.id = 1 со значением 1.0
        self.assertEqual(xrate.rate, FOR_TEST_DB['rate'])
        test_api.update_xrates(FOR_TEST_DB['from_currency'], FOR_TEST_DB['to_currency'])
        xrate = model.ExRate.get(id = 1)
        # сравнить xrate.id = 1 со значением 1.01 (update_xrates увеличивает значение rate на 0.01)
        self.assertEqual(xrate.rate, 1.01)

if __name__ == "__main__":
    unittest.main()