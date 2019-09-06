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
    try:
        if ptts.tt_active_user:
            for key, value in ptts.tt_active_user.get('cookies').items():
                cookies += key + "=" + value + "; "
        else:
            cookies = "null = 1;"
        url_parse = parse.urlsplit(url)
        headers = {
            "Accept-Encoding": "gzip",
            "sdk-version": "1",
            "Cookie": cookies,
            'X-SS-REQ-TICKET': '1541500434739',
            'X-SS-TC': '0',
            "x-tt-token": "002447bd7d6a5c792cb223b1151e399e0402e5fdcf768ab9f96930b63dc169d353480340ec7abaa1856d8133dcfe12363b42",
            "Host": url_parse.netloc,
            "Connection": "Keep-Alive",
            "User-Agent": "com.ss.android.ugc.trill/584 (Linux; U; Android 5.1.1; en_US; LG-H961N;",
        }

        if request_type:
            if request_type == "post":
                return requests.post(url, headers=headers, data=posts, timeout=5)
            elif request_type == "get":
                return requests.get(url, headers=headers, timeout=5)
        else:
            raise Exception("Missing request type. Must be GET or POST.")
    except Exception as e:
        logger.error("An error occurred: {}".format(str(e)))
        return None

def make_request_tta(url, posts=None, request_type=None):
    try:
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-encoding": "gzip, deflate, br",
            "user-agent": Constants.REQUESTS_VIDEO_UA.get("User-Agent"),
            "cache-control": "max-age=0",
        }

        if request_type:
            if request_type == "post":
                return requests.post(url, headers=headers, data=posts, timeout=5)
            elif request_type == "get":
                return requests.get(url, headers=headers, timeout=5)
        else:
            raise Exception("Missing request type. Must be GET or POST.")
    except Exception as e:
        logger.error("An error occurred: {}".format(str(e)))
        return None

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
