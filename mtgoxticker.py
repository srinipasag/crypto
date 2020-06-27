import base64, hashlib, hmac, urllib2, time, urllib, json
import logging

base = 'https://data.mtgox.com/api/2/'

API_KEY='3fc4e875-6bab-4b7c-b740-2d8ea3225400'
SECRET='TwoxLAcKcCdqzD7Fc0ClKX/v37vsF0EaGVTMefslc2kYPkUZJgvdxTEaT2xG1R/ocarWU/Qoyq8vUnMJTiCLnA=='


REFRESH_TIME_SECONDS=60
LOG_FILE_NAME='mtgoxticker.log'


### LOGGING CONF################################
logging.basicConfig()
logger = logging.getLogger('mtgoxticker')
logger.setLevel('DEBUG')
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create file handler
fh = logging.FileHandler(LOG_FILE_NAME)
fh.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
#add formatter to fh
fh.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)
# and fh
logger.addHandler(fh)
#################################################


def post_request(key, secret, path, data):
    hmac_obj = hmac.new(secret, path + chr(0) + data, hashlib.sha512)
    hmac_sign = base64.b64encode(hmac_obj.digest())

    header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'gox2 based client',
        'Rest-Key': key,
        'Rest-Sign': hmac_sign,
    }

    request = urllib2.Request(base + path, data, header)
    response = urllib2.urlopen(request, data)
    return json.load(response)


def gen_tonce():
    return str(int(time.time() * 1e6))


class MtGox:

    def __init__(self, key, secret):
        self.key = key
        self.secret = base64.b64decode(secret)

    def request(self, path, params={}):
        params = dict(params)
        params['tonce'] = gen_tonce()
        data = urllib.urlencode(params)

        result = post_request(self.key, self.secret, path, data)
        if result['result'] == 'success':
            return result['data']
        else:
            raise Exception(result['result'])


m = MtGox(API_KEY, SECRET)
def go():
    while True:
        ticker = m.request('BTCUSD/money/ticker')
        ticker = json.dumps(ticker)
        data = 'Result=%s' % (ticker)
        logger.info(data)
        time.sleep(REFRESH_TIME_SECONDS)

if __name__ == "__main__":
    go()

