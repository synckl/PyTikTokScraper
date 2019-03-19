import sys
import time
import random
try:
    import helpers
except ImportError:
    from . import helpers


class Constants:
    """"
    Some of the endpoints used by TikTok.
    We'll probably only use the Login endpoint and the User Post Feed endpoint.
    """""
    BASE_URL = "https://api2.musical.ly/"
    VIDEO_BASE_URL = "https://api2.musical.ly/aweme/v1/play/?video_id={" \
                     ":s}&line=1&ratio=540p&media_type=4&vr_type=0&test_cdn=None&improve_bitrate={:d}"
    LOGIN_ENDP = "passport/user/login/?"
    FEED_ENDP = "aweme/v1/feed/?count=20&offset=0&max_cursor=0&type=0&is_cold_start=1&pull_type=1&"
    DISCOVER_ENDP = "aweme/v1/discover/search/?cursor=0&keyword={:s}&count=10&type=1&hot_search=0&"
    LIKE_STATUS_ENDP = "aweme/v1/commit/item/digg/?aweme_id={:d}&type={:d}&retry_type=no_retry&from=3&"
    FOLLOW_STATUS_ENDP = "aweme/v1/commit/follow/user/?user_id={:s}&type={:d}&retry_type=no_retry&from=3&"
    POST_INFO_ENDP = "aweme/v1/aweme/stats/?"
    USER_INFO_ENDP = "aweme/v1/user/?user_id={:d}&"
    USER_POST_FEED_ENDP = "aweme/v1/aweme/post/?user_id={:s}&type=0&count=20&pull_type=1&max_cursor={:d}&"
    USER_FOLLOWING_ENDP = "aweme/v1/user/following/list/?user_id={:s}&offset=0&count=1000&max_time=" + str(int(time.time())) + "&source_type=2&"

    LIVE_ROOM_ENDP = 'aweme/v1/room/enter/?room_id={:d}&'
    LIVE_FLV_ENDP = 'http://pull-flv-l1-mus.pstatp.com/hudong/stream-{}.flv'
    LIVE_HLS_ENDP = 'http://pull-hls-l1-mus.pstatp.com/hudong/stream-{}/playlist.m3u8'
    LIVE_WEB_URL = 'https://m.tiktok.com/share/live/{}/?language=en'

    """
    We'll just keep these constants here for the sake of tidiness
    """
    PYTHON_VER = sys.version.split(' ')[0]
    SCRIPT_VER = "1.3"

    """
    Device variables.
    """

    DEVICE_VARS = {'app_language': "en", 'language': "en", 'region': "tr", 'app_type': "normal", 'sys_region': "TR",
                   'carrier_region': "TR", 'carrier_region_v2': "286", 'build_number': "8.4.0",
                   'timezone_offset': "10800", 'timezone_name': "Europe/Istanbul", 'mcc_mnc': "28601", 'is_my_cn': "0",
                   'fp': "", 'account_region': "TR", 'iid': random.randint(20000000000, 35000000000), 'ac': "wifi",
                   'channel': "googleplay", 'aid': "1233", 'app_name': "musical_ly", 'version_code': "840",
                   'version_name': "8.4.0", 'device_id': random.randint(35000000000, 50000000000), 'device_platform': "android",
                   'ssmix': "a", 'device_type': "TA-1020", 'device_brand': "Nokia", 'os_api': "26",
                   'os_version': "8.0.0", 'openudid': ''.join([random.choice(list('0123456789abcdef')) for i in range(16)]), 'manifest_version_code': "2018090613",
                   'resolution': "720*1280", 'dpi': "320", 'update_version_code': "2018090613", 'uuid': '863' + str(random.randint(200000000000, 350000000000)),
                   }

    REQUESTS_UA = {'User-Agent': "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/60.0.3112.90 Safari/537.36"}
