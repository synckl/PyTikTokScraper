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
    USER_INFO_ENDP = "aweme/v1/user/?user_id={:d}&"
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
    SCRIPT_VER = "1.6"

    """
    Device variables.
    """

    DEVICE_VARS = {
        "js_sdk_version": "",
        "app_type": "normal",
        "os_api": "22",
        "device_type": "SM-G920F",
        "ssmix": "a",
        "manifest_version_code": "2019011531",
        "dpi": "420",
        "carrier_region": "NL",
        "region": "US",
        "carrier_region_v2": "",
        "app_name": "musical_ly",
        "version_name": "9.9.0",
        "ab_version": "9.9.0",
        "timezone_offset": "28800",
        "pass-route": "1",
        "pass-region": "1",
        "is_my_cn": "0",
        "fp": "TlTrLSLMLzwSFl5rF2U1LSFIcrGe",
        "ac": "wifi",
        "update_version_code": "2019011531",
        "channel": "googleplay",
        "device_platform": "android",
        "iid": "6661938120256931589",
        "build_number": "9.9.0",
        "version_code": "990",
        "timezone_name": "Asia/Shanghai",
        "openudid": "9479023183233382",
        "device_id": "6661937182847157766",
        "sys_region": "US",
        "app_language": "en",
        "resolution": "1080*1920",
        "os_version": "5.1.1",
        "device_brand": "samsung",
        "language": "en",
        "aid": "1233",
        "mcc_mnc": "20404",
        "as": "a165194f0f0d7ccca26455",
        "cp": "99d2c15ff120f5cee1[cIg",
        "mas": "01ced3034f4e7feb1f2b774417ce9d3fdcacac2c6c4c86c6c6c6e",
        "_rticket": str(int(time.time())),
        "ts": str(int(time.time())),
    }

    REQUESTS_VIDEO_UA = {'User-Agent': "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/60.0.3112.90 Safari/537.36"}
