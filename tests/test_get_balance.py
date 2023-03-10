import unittest
import os
from okxpy import OKX

API_KEY = os.getenv("API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
API_PASSPHRASE = os.getenv("API_PASSPHRASE")

class TestGetBalance(unittest.TestCase):
    def test_get_balance(self):
        okx = OKX(API_KEY, API_SECRET_KEY, API_PASSPHRASE)
        response = {
            "code": "0",
            "msg": "",
            "data": [
                {
                    "availBal": "37.11827078",
                    "bal": "37.11827078",
                    "ccy": "ETH",
                    "frozenBal": "0"
                }
            ]
        }
        self.assertEqual(okx.get_account_balance(), response)


unittest.main()