import unittest
import requests
import json
import pprint
import logging
from blockchain.statistics import *

class TestApis(unittest.TestCase):
    def test_statsApi(self):
        response = requests.get("https://api.blockchain.info/stats")
        result = response.json()
        #pprint.pprint(result)

    def test_chartsApi(self):
        #response = requests.get("https://api.blockchain.info/charts/transactions-per-second?timespan=5weeks&rollingAverage=8hours&format=json")
        response = requests.get("https://blockchain.info/unconfirmed-transactions?format=json")
        result = response.json()
        #pprint.pprint(result)
        #for key,value in result.items():
            #print(key,":",value)

class TestBitMinter(unittest.TestCase):

    def test_bitminter_stats(self):
        h = {
            'Authorization': 'key=0FBQIY3BXF4UYMPHPXR0D1PZFZRRCPHL'
        }
        #r = requests.get('https://bitminter.com/api/pool/stats')
        r = requests.get('https://bitminter.com/api/pool/blocks?commodity = BTC & max = 20')

        data = 'ResponseCode="%s" Result=%s' % (r.status_code, r.text)
        print("test_bitminter_stATS")
        pprint.pprint(data)

    def test_bitminter_users(self):
        h = {
            'Authorization': 'key=0FBQIY3BXF4UYMPHPXR0D1PZFZRRCPHL'
        }
        r = requests.get('https://bitminter.com/api/users', headers=h)
        data = 'ResponseCode="%s" Result=%s' % (r.status_code, r.text)
        print("test_bitminter_users")
        pprint.pprint(data)


if __name__ == '__main__':
    unittest.main()