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
    BASE_URL = "https://api2-19-h2.musical.ly/"
    VIDEO_BASE_URL = "https://api2.musical.ly/aweme/v1/play/?video_id={" \
                     ":s}&line=1&ratio=540p&media_type=4&vr_type=0&test_cdn=None&improve_bitrate={:d}"
    LOGIN_ENDP = "passport/user/login/?"
    FEED_ENDP = "aweme/v1/feed/?count=20&offset=0&max_cursor=0&type=0&is_cold_start=1&pull_type=1&max_cursor={:d}&"
    HASHTAG_SEARCH_ENDP = "aweme/v1/challenge/search/?cursor=0&keyword=%23{:s}&count=1&hot_search=0&is_pull_refresh=0&search_source=challenge&"
    HASHTAG_FEED_ENDP = "aweme/v1/challenge/aweme/?ch_id={:s}&query_type=0&cursor={:d}&type=5&retry_type=no_retry&"
    DISCOVER_ENDP = "aweme/v1/discover/search/?cursor=0&keyword={:s}&count=10&type=1&is_pull_refresh=0&hot_search=0&search_source&"
    DISCOVER_TTA_ENDP = "https://tiktokapi.ga/php/jsonusr.php?q={:s}&cursor=0"
    LIKE_STATUS_ENDP = "aweme/v1/commit/item/digg/?aweme_id={:d}&type={:d}&retry_type=no_retry&from=3&"
    FOLLOW_STATUS_ENDP = "aweme/v1/commit/follow/user/?user_id={:s}&type={:d}&retry_type=no_retry&from=3&"
    POST_INFO_ENDP = "aweme/v1/aweme/stats/?"
    USER_INFO_ENDP = "aweme/v1/user/?user_id={:s}&"
    USER_POST_FEED_ENDP = "aweme/v1/aweme/post/?user_id={:s}&type=0&count=20&pull_type=1&max_cursor={:d}&"
    USER_FOLLOWING_ENDP = "aweme/v1/user/following/list/?user_id={:s}&offset=0&count=1000&max_time=" + str(
        int(time.time())) + "&source_type=2&"

    LIVE_ROOM_ENDP = 'aweme/v1/room/enter/?room_id={:d}&'
    LIVE_FLV_ENDP = 'http://pull-flv-l1-mus.pstatp.com/hudong/stream-{}.flv'
    LIVE_HLS_ENDP = 'http://pull-hls-l1-mus.pstatp.com/stage/stream-{}/playlist.m3u8'
    LIVE_WEB_URL = 'https://m.tiktok.com/share/live/{}/?language=en'

    """
    We'll just keep these constants here for the sake of tidiness
    """
    PYTHON_VER = sys.version.split(' ')[0]
    SCRIPT_VER = "1.7"

    """
    Device variables.
    """

    DEVICE_VARS = {
        "ts": "1556178331",
        "js_sdk_version": "",
        "app_type": "normal",
        "manifest_version_code": "583",
        "_rticket": "1556178332328",
        "app_language": "en",
        "iid": "6683055906148435713",
        "channel": "googleplay",
        "device_type": "MIX%202",
        "language": "en",
        "account_region": "VN",
        "resolution": "1080*2030",
        "openudid": "b19f5ff713b925ef",
        "update_version_code": "5830",
        "sys_region": "US",
        "os_api": "26",
        "uoo": "0",
        "is_my_cn": "0",
        "timezone_name": "Asia%2FHo_Chi_Minh",
        "dpi": "440",
        "carrier_region": "VN",
        "ac": "wifi",
        "device_id": "6620810330052445697",
        "pass-route": "1",
        "mcc_mnc": "45204",
        "os_version": "8.0.0",
        "timezone_offset": "25200",
        "version_code": "583",
        "carrier_region_v2": "452",
        "app_name": "trill",
        "ab_version": "5.8.3",
        "version_name": "5.8.3",
        "device_brand": "Xiaomi",
        "ssmix": "a",
        "pass-region": "1",
        "device_platform": "android",
        "build_number": "5.8.3",
        "region": "US",
        "aid": "1180",
        "as": "a1qwert123",
        "cp": "cbfhckdckkde1"
    }

    REQUESTS_VIDEO_UA = {'User-Agent': "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/60.0.3112.90 Safari/537.36"}
