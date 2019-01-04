import os
import json

try:
    import helpers
    import ptts
    from constants import Constants
except ImportError:
    from . import helpers
    from . import ptts
    from .constants import Constants


def login(username, password):
    username = helpers.xor(username)
    password = helpers.xor(password)
    
    if not os.path.exists(ptts.cookies_path):
        os.makedirs(ptts.cookies_path)

    cookie_path = os.path.join(ptts.cookies_path, username + ".json")
    if os.path.isfile(cookie_path):
        with open(cookie_path) as cookie_file:
            active_user_cookie = json.load(cookie_file)
            if active_user_cookie.get('data').get('user_id'):
                ptts.tt_active_user = active_user_cookie
                return

    posts = {
        'mix_mode':1,
        'username':username,
        'password':password,
        'email': None,
        'mobile': None,
        'account': None,
        'captcha': None
    }

    request_url = Constants.BASE_URL + Constants.LOGIN_ENDP + helpers.query(Constants.DEVICE_VARS)
    request_response = helpers.make_request(request_url, posts, request_type="post")

    try:
        headers = {}
        for c in request_response.cookies:
            headers[c.name]= c.value

    except KeyError:
        headers = None
    response_json = {}
    if request_response.status_code != 200:
        return False
    else:
        data = request_response.json()
        if data.get('data') and not data.get('error_code'):
            response_json['data'] = helpers.user_data_export(data.get('data'))
            response_json['cookies'] = headers
            with open(cookie_path, 'w') as outfile:
                json.dump(response_json, outfile)
                ptts.tt_active_user = response_json
            return True
        else:
            ptts.tt_active_user = response_json
            return True


def search_user(username):
    request_url = Constants.BASE_URL + Constants.DISCOVER_ENDP.format(username) + helpers.query(Constants.DEVICE_VARS)
    request_response = helpers.make_request(request_url, request_type="get")
    return request_response.json()


def user_post_feed(user_id, max_cursor=0):
    request_url = Constants.BASE_URL + Constants.USER_POST_FEED_ENDP.format(user_id, max_cursor) + helpers.query(Constants.DEVICE_VARS)
    request_response = helpers.make_request(request_url, request_type="get")
    return request_response.json()


def get_live_feed(live_room_id):
    request_url = Constants.BASE_URL + Constants.LIVE_ROOM_ENDP.format(live_room_id) + helpers.query(Constants.DEVICE_VARS)
    request_response = helpers.make_request(request_url, request_type="get")
    return request_response.json()


def get_following(target_user_id):
    request_url = Constants.BASE_URL + Constants.USER_FOLLOWING_FNDP.format(target_user_id) + helpers.query(Constants.DEVICE_VARS)
    request_response = helpers.make_request(request_url, request_type="get")
    return request_response.json()
