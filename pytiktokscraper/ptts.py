import os

def noinit(self):
    pass


def initialize():
    global tt_username
    global tt_password
    global tt_target_user
    global tt_target_id
    global tt_active_user
    global dl_path
    global cookies_path
    global args
    tt_username = None
    tt_password = None
    tt_target_user = None
    tt_target_id = None
    tt_active_user = {}
    dl_path = os.getcwd()
    cookies_path = os.path.join(os.getcwd(), 'cookies')
    args = None
