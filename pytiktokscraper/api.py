import os
import json
import sys

try:
    import helpers
    import ptts
    from constants import Constants
except ImportError:
    from . import helpers
    from . import ptts
    from .constants import Constants


def login(username=None, password=None):
#     username = helpers.xor(username)
#     password = helpers.xor(password)
    
#     if not os.path.exists(ptts.cookies_path):
#         os.makedirs(ptts.cookies_path)

    cookie_path = os.path.join(ptts.cookies_path, "cookie.json")
    if os.path.isfile(cookie_path):
        with open(cookie_path) as cookie_file:
            active_user_cookie = json.load(cookie_file)
            ptts.tt_active_user = active_user_cookie
            return

#     posts = {
#         'mix_mode':1,
#         'username':username,
#         'password':password,
#         'email': None,
#         'mobile': None,
#         'account': None,
#         'captcha': None
#     }

#     request_url = Constants.BASE_URL + Constants.LOGIN_ENDP + helpers.query(Constants.DEVICE_VARS)
#     request_response = helpers.make_request(request_url, posts, request_type="post")

#     try:
#         headers = {}
#         for c in request_response.cookies:
#             headers[c.name]= c.value

#     except KeyError:
#         headers = None
#     response_json = {}
#     if request_response.status_code != 200:
#         return False
#     else:
#         data = request_response.json()
#         if data.get('data') and not data.get('error_code'):
#             response_json['data'] = helpers.user_data_export(data.get('data'))
#             response_json['cookies'] = headers
#             with open(cookie_path, 'w') as outfile:
#                 json.dump(response_json, outfile)
#                 ptts.tt_active_user = response_json
#             return True
#         else:
#             ptts.tt_active_user = response_json
#             return True


def search_user(username):
    request_url = Constants.BASE_URL + Constants.DISCOVER_ENDP.format(username) + helpers.query(Constants.DEVICE_VARS)
    #as_cp = ptts.signature_gen.generate_as_cp(request_url, helpers.get_timestamp())
    #request_url = request_url + "&as={:s}&cp={:s}".format(as_cp[0], as_cp[1])
    #request_url = request_url + "&as=a1qwert123&cp=cbfhckdckkde1&mas=01937dea4a12a8c410eb526555c121d44decec4c0ccc0c8666c61c"
    request_response = helpers.make_request(request_url, request_type="get")
    return request_response.json() if request_response else None

def get_user_info(user_id):
    request_url = Constants.BASE_URL + Constants.USER_INFO_ENDP.format(user_id) + helpers.query(Constants.DEVICE_VARS)
    #as_cp = ptts.signature_gen.generate_as_cp(request_url, helpers.get_timestamp())
    #request_url = request_url + "&as={:s}&cp={:s}".format(as_cp[0], as_cp[1])
    #request_url = request_url + "&as=a1qwert123&cp=cbfhckdckkde1&mas=01937dea4a12a8c410eb526555c121d44decec4c0ccc0c8666c61c"
    request_response = helpers.make_request(request_url, request_type="get")
    return request_response.json() if request_response else None

def search_user_tta(username):
    request_url = Constants.DISCOVER_TTA_ENDP.format(username)
    request_response = helpers.make_request_tta(request_url, request_type="get")
    return request_response.json() if request_response else None


def user_post_feed(user_id, max_cursor=0):
    request_url = Constants.BASE_URL + Constants.USER_POST_FEED_ENDP.format(user_id, max_cursor) + helpers.query(Constants.DEVICE_VARS)
    # as_cp = ptts.signature_gen.generate_as_cp(request_url, helpers.get_timestamp())
    # request_url = request_url + "&as={:s}&cp={:s}".format(as_cp[0], as_cp[1])
    request_response = helpers.make_request(request_url, request_type="get")
    return request_response.json() if request_response else None


def get_live_feed(live_room_id):
    request_url = Constants.BASE_URL + Constants.LIVE_ROOM_ENDP.format(live_room_id) + helpers.query(Constants.DEVICE_VARS)
    # as_cp = ptts.signature_gen.generate_as_cp(request_url, helpers.get_timestamp())
    # request_url = request_url + "&as={:s}&cp={:s}".format(as_cp[0], as_cp[1])
    request_response = helpers.make_request(request_url, request_type="get")
    return request_response.json() if request_response else None


def get_following(target_user_id):
    request_url = Constants.BASE_URL + Constants.USER_FOLLOWING_FNDP.format(target_user_id) + helpers.query(Constants.DEVICE_VARS)
    # as_cp = ptts.signature_gen.generate_as_cp(request_url, helpers.get_timestamp())
    # request_url = request_url + "&as={:s}&cp={:s}".format(as_cp[0], as_cp[1])
    request_response = helpers.make_request(request_url, request_type="get")
    return request_response.json() if request_response else None

def hashtag_feed(hashtag_id, cursor=0):
    request_url = Constants.BASE_URL + Constants.HASHTAG_FEED_ENDP.format(hashtag_id, cursor) + helpers.query(Constants.DEVICE_VARS)
    # as_cp = ptts.signature_gen.generate_as_cp(request_url, helpers.get_timestamp())
    # request_url = request_url + "&as={:s}&cp={:s}".format(as_cp[0], as_cp[1])
    request_response = helpers.make_request(request_url, request_type="get")
    return request_response.json() if request_response else None

def hashtag_search(text):
    request_url = Constants.BASE_URL + Constants.HASHTAG_SEARCH_ENDP.format(text) + helpers.query(Constants.DEVICE_VARS)
    # as_cp = ptts.signature_gen.generate_as_cp(request_url, helpers.get_timestamp())
    # request_url = request_url + "&as={:s}&cp={:s}".format(as_cp[0], as_cp[1])
    request_response = helpers.make_request(request_url, request_type="get")
    return request_response.json() if request_response else None
