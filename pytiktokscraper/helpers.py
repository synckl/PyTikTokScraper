import time
from urllib import parse
import requests
import subprocess
import os
import hashlib

try:
    import ptts
    import logger
    import helpers
    from constants import Constants
except ImportError:
    from . import ptts
    from . import helpers
    from . import logger
    from .constants import Constants


def strdatetime():
    return time.strftime('%m-%d-%Y %I:%M:%S %p')


def strtime():
    return time.strftime('%I:%M:%S %p')


def strdate():
    return time.strftime('%m-%d-%Y')


def call_ytdl(url, filename):
    try:
        subprocess.call('youtube-dl -o "{}.mp4" "{}"'.format(filename, url), shell=True)
        return True
    except Exception as e:
        logger.separator()
        logger.error("Something went wrong: " + str(e))
        logger.separator()
        if os.path.isfile(filename + '.mp4.part'):
            os.rename(filename + '.mp4.part', filename + '.mp4')
    except KeyboardInterrupt:
        logger.separator()
        logger.info("The download has been aborted.")
        if os.path.isfile(filename + '.mp4.part'):
            os.rename(filename + '.mp4.part', filename + '.mp4')
        logger.separator()


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
        "X-SS-STUB": "65812F1862DA48711939361C1D7DDE2B",
        "Accept-Encoding": "gzip",
        "sdk-version": "1",
        "Cookie": cookies,
        "x-tt-token": "03804231875ca4f8e91cc80235d8d3d6b311d0b3873a40b558862491a9e504cff48d3604600865f84d6609acb43944031f9",
        "X-Gorgon": "03006cc00000ca82ae964c86eee4216c66f887ee07f6f1cf7fb5",
        "X-Khronos": str(int(time.time())),
        "X-Pods": "",
        "Host": url_parse.netloc,
        "Connection": "Keep-Alive",
        "User-Agent": "com.zhiliaoapp.musically/2018111632 (Linux; U; Android 8.0.0; nl_NL; ONEPLUS A3003; Build/OPR1.170623.032; Cronet/58.0.2991.0)",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Forwarded-For": requests.get("https://api.ipify.org/?format=text").text
    }

    if request_type:
        if request_type == "post":
            return requests.post(url, headers=headers, data=posts)
        elif request_type == "get":
            return requests.get(url, headers=headers)
    else:
        raise Exception("Missing request type. Must be GET or POST.")


def get_timestamp():
    return int(round(time.time() * 1000))


class CalcSig(object):
    key1 = '57218436'
    key2 = '15387264'
    rstr = 'efc84c17'

    def shuffle(self, p1, p2):
        p = ''
        p += p1[int(p2[0], 10) - 1]
        p += p1[int(p2[1], 10) - 1]
        p += p1[int(p2[2], 10) - 1]
        p += p1[int(p2[3], 10) - 1]
        p += p1[int(p2[4], 10) - 1]
        p += p1[int(p2[5], 10) - 1]
        p += p1[int(p2[6], 10) - 1]
        p += p1[int(p2[7], 10) - 1]
        return p.lower()

    def get_as_cp(self, u_md5, u_key1, u_key2):
        ascp = list()
        for i in range(36):
            ascp.append(0)
        ascp[0] = 'a'
        ascp[1] = '1'
        for i in range(0, 8):
            ascp[2 * (i + 1)] = u_md5[i]
            ascp[2 * i + 3] = u_key2[i]
            ascp[2 * i + 18] = u_key1[i]
            ascp[2 * i + 1 + 18] = u_md5[i + 24]
        ascp[-2] = 'e'
        ascp[-1] = '1'

        return ''.join(ascp)

    def parseURL(self, url):
        param_index = url.find('?')
        param = url[param_index + 1:]
        param_list = param.split('&')
        param_list.append('rstr=' + self.rstr)
        param_list = sorted(param_list)
        result = ''
        for a in param_list:
            tmp = a.split('=')
            tmp[1] = tmp[1].replace('+', 'a')
            tmp[1] = tmp[1].replace(' ', 'a')
            result += tmp[1]
        return result

    def calcMD5(self, str_encode):
        m = hashlib.md5()
        m.update(str_encode.encode('utf-8'))
        return m.hexdigest()

    def generate_as_cp(self, url, curtime):
        url_param = self.parseURL(url)
        p_md5 = self.calcMD5(url_param)
        if curtime & 1:
            p_md5 = self.calcMD5(p_md5)
        hexTime = hex(curtime)[2:]
        aa = self.shuffle(hexTime, self.key1)
        bb = self.shuffle(hexTime, self.key2)
        sig = self.get_as_cp(p_md5, aa, bb)
        return sig[:18], sig[18:]
