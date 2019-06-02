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
            "Cookie": "cookies",
            "x-tt-token": "03aa7fe52bf9eae34e66d2ae1aae56a9d198947aaffbdfe62122332ef637fea45596abd9673d432a9876e4eeb55248c1e40",
            "Host": url_parse.netloc,
            "Connection": "Keep-Alive",
            "User-Agent": "okhttp/3.10.0.1",
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
