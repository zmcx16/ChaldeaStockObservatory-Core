import requests

from common import *


def send_request(url):
    try:
        res = requests.get(url)
        res.raise_for_status()
    except Exception as exc:
        print('Generated an exception: %s' % exc)
        return ERR_WEB_ERROR, exc

    return ERR_SUCCESS, res.text

