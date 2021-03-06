import os
import time
try:
    import helpers
except ImportError:
    from . import helpers


def noinit(self):
    pass


def initialize():
    global tt_username
    global tt_password
    global tt_target_user
    global tt_target_id
    global tt_active_user
    global tt_target_hashtag
    global dl_path
    global cookies_path
    global args
    global epochtime
    global signature_gen
    global tt_target_user_liveroomid
    tt_username = None
    tt_password = None
    tt_target_user = None
    tt_target_id = None
    tt_target_hashtag = None
    tt_active_user = {}
    dl_path = os.getcwd()
    cookies_path = os.path.join(os.getcwd(), 'cookies')
    args = None
    epochtime = str(time.time())
    signature_gen = helpers.CalcSig()
    tt_target_user_liveroomid = None