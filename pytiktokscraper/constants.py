import sys
import time


class Constants:
    """"
    Some of the endpoints used by TikTok.
    We'll probably only use the Login endpoint and the User Post Feed endpoint.
    """""
    BASE_URL = "https://api2.musical.ly/"
    VIDEO_BASE_URL = "https://api2.musical.ly/aweme/v1/play/?video_id={" \
                     ":s}&line=1&ratio=540p&media_type=4&vr_type=0&test_cdn=None&improve_bitrate=1 "
    LOGIN_ENDP = "passport/user/login/?"
    FEED_ENDP = "aweme/v1/feed/?count=20&offset=0&max_cursor=0&type=0&is_cold_start=1&pull_type=1&"
    DISCOVER_ENDP = "aweme/v1/discover/search/?cursor=0&keyword={:s}&count=10&type=1&hot_search=0&"
    LIKE_STATUS_ENDP = "aweme/v1/commit/item/digg/?aweme_id={:d}&type={:d}&retry_type=no_retry&from=3&"
    FOLLOW_STATUS_ENDP = "aweme/v1/commit/follow/user/?user_id={:s}&type={:d}&retry_type=no_retry&from=3&"
    POST_INFO_ENDP = "aweme/v1/aweme/stats/?"
    USER_INFO_ENDP = "aweme/v1/user/?user_id={:d}&"
    USER_POST_FEED = "aweme/v1/aweme/post/?user_id={:s}&type=0&count=20&pull_type=1&max_cursor={:d}&"

    """
    We'll just keep these constants here for the sake of tidiness
    """
    PYTHON_VER = sys.version.split(' ')[0]
    SCRIPT_VER = "1.0"

    """
    Device variables.
    """
    DEVICE_VARS = {'app_language': "en", 'language': "en", 'region': "au", 'app_type': "normal", 'sys_region': "AU",
                   'carrier_region': "AU", 'carrier_region_v2': "286", 'build_number': "96104",
                   'timezone_offset': "28800", 'timezone_name': "Australia/Sydney", 'mcc_mnc': "50502", 'is_my_cn': "1",
                   'fp': "", 'account_region': "&", 'iid': "6620659482206930694", 'ac': "4G", 'channel': "App%20Store",
                   'aid': "1233", 'app_name': "musical_ly", 'version_code': "9.6.1", 'version_name': "8.4.0",
                   'device_id': "6623534804040304133", 'device_platform': "iphone", 'ssmix': "a",
                   'device_type': "iPhone11,2", 'device_brand': "Apple", 'os_api': "18", 'os_version': "12.1",
                   'openudid': "bdb28a05d14cf194ad2336d13d2409e2b8e2b43a", 'manifest_version_code': "2018090613",
                   'resolution': "720*1280", 'dpi': "320", 'update_version_code': "2018090613",
                   '_rticket': int(round(time.time() * 1000)), 'ts': int(round(time.time() * 1000)), 'as': "a1qwert123",
                   'cp': "cbfhckdckkde1"}

    REQUESTS_UA = {'User-Agent': "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/60.0.3112.90 Safari/537.36"}
