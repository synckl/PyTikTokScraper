import time
from urllib import parse
import requests
import json

try:
    import ptts
except ImportError:
    from . import ptts

def strdatetime():
    return time.strftime('%m-%d-%Y %I:%M:%S %p')


def strtime():
    return time.strftime('%I:%M:%S %p')


def strdate():
    return time.strftime('%m-%d-%Y')


def xor(input, key=5):
    variable = []
    result = ""
    for x in range(len(input)):
        variable.append(ord(input.__getitem__(x)) ^ key)
    for c in variable:
        result += base_convert(number=c, toBase=16)
    return result


def base_convert(number, toBase):
    if toBase < 2 or toBase > 36:
        raise NotImplementedError

    try:
        base10 = number
    except ValueError:
        raise

    digits = '0123456789abcdefghijklmnopqrstuvwxyz'
    sign = ''

    if base10 == 0:
        return '0'
    elif base10 < 0:
        sign = '-'
        base10 = -base10

    # Convert to base toBase
    s = ''
    while base10 != 0:
        r = base10 % toBase
        r = int(r)
        s = digits[r] + s
        base10 //= toBase

    output_value = sign + s
    return output_value


def query(data):
    return parse.urlencode(data)


def user_data_export(data):
    data_export = {'user_id': data.get('user_id'), 'session_key': data.get('session_key'),
                   'screen_name': data.get('screen_name')}
    return data_export


def make_request(url, posts=None, request_type=None):
    cookies = ""
    if ptts.tt_active_user:
        for key, value in ptts.tt_active_user.get('cookies').items():
            cookies += key + "=" + value + "; "
    else:
        cookies = "null = 1;"
    url_parse = parse.urlsplit(url)
    headers = {
        "Host": url_parse.netloc,
        'X-SS-TC': "0",
        'User-Agent': "com.zhiliaoapp.musically/2018090613 (Linux; U; Android 8.0.0; tr_TR; TA-1020; Build/O00623; "
                      "Cronet/58.0.2991.0)",
        'Accept-Encoding': "gzip",
        'Connection': "keep-alive",
        'X-Tt-Token': "",
        'sdk-version': "1",
        'Cookie': cookies
    }
    if request_type:
        if request_type == "post":
            return requests.post(url, headers=headers, data=posts)
        elif request_type == "get":
            return requests.get(url, headers=headers)
    else:
        raise Exception("Missing request type. Must be GET or POST.")
