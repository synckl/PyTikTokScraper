import requests
import re
import os
import json
from mutagen.mp4 import MP4

try:
    import ptts
    import logger
    import api
    import helpers
    from constants import Constants
except ImportError:
    from . import ptts
    from . import api
    from . import logger
    from . import helpers
    from .constants import Constants


def download_all(target_user_id):
    try:
        max_cursor = 0
        has_more = 0
        downloaded_total = 0
        checked_total = 0
        available_total = 0
        current_feed_page = 1

        if not os.path.exists(os.path.join(ptts.dl_path, ptts.tt_target_user)):
            os.makedirs(os.path.join(ptts.dl_path, ptts.tt_target_user))

        download_path = os.path.join(ptts.dl_path, ptts.tt_target_user)
        while True:
            if ptts.args.recent:
                logger.separator()
                logger.binfo("Only checking the first 10 videos (--recent was passed).")
            if not has_more and not max_cursor:
                logger.separator()
                logger.info("Retrieving first feed page (page {:d})".format(current_feed_page))
                logger.separator()
            json_data = api.user_post_feed(user_id=target_user_id, max_cursor=max_cursor)
            max_cursor = json_data.get('max_cursor')
            has_more = json_data.get('has_more')
            if not json_data.get("aweme_list", None):
                if checked_total:
                    logger.separator()
                    logger.info("End of feed reached. {:d} {:s} been downloaded.".format(
                        downloaded_total, "video has" if downloaded_total == 1 else "videos have"))
                elif not checked_total:
                    logger.info("There are no available videos to download.")
                logger.separator()
                break
            else:
                current_feed_page += 1
                available_total += len(json_data.get("aweme_list")) if not ptts.args.recent else 10
                for video in json_data.get("aweme_list"):
                    if ptts.args.recent and checked_total == 10:
                        if downloaded_total:
                            logger.separator()
                            logger.info("10 videos have been checked. {:d} {:s} been downloaded.".format(
                                downloaded_total, "video has" if downloaded_total == 1 else "videos have"))
                        else:
                            logger.info("10 videos have been checked. There are no available videos to download.")
                        logger.separator()
                        return
                    else:
                        video_uri = video.get("video").get("play_addr").get("uri")
                        video_desc = video.get("desc")
                        filename = '{:d}_{:s}.mp4'.format(video.get("create_time"), video.get("author").get("unique_id"))
                        if video_uri.isdigit():
                            actual_video_uri = video.get("video").get("play_addr").get("url_list")[0]
                            if not os.path.isfile(os.path.join(download_path, filename)):

                                rr = requests.get(actual_video_uri, verify=True)
                                if rr.status_code == 200:
                                    open(os.path.join(download_path, filename), 'wb').write(rr.content)
                                    try:
                                        mp4_video_tags = MP4(os.path.join(download_path, filename))
                                        mp4_video_tags['\xa9cmt'] = video_desc
                                        mp4_video_tags.save()
                                    except Exception as e:
                                        pass
                                    logger.info(
                                        "({:d}/{:d}) - Downloaded video with Id: {}".format(checked_total + 1,
                                                                                            available_total,
                                                                                            video_uri))
                                    downloaded_total += 1
                                else:
                                    logger.warn("Response did not return status 200, was {:d} instead. Giving up and "
                                                "moving on.".format(rr.status_code))
                                    logger.warn("The video Id was: {:s}".format(video_uri))
                            else:
                                logger.info("({:d}/{:d}) - Already downloaded video with Id: {}".format(checked_total + 1,
                                                                                                        available_total,
                                                                                                        video_uri))
                        else:
                            if not os.path.isfile(os.path.join(download_path, filename)):
                                rr = requests.get(Constants.VIDEO_BASE_URL.format(video_uri, 1), verify=True, headers=Constants.REQUESTS_VIDEO_UA)
                                if rr.status_code == 200:
                                    open(os.path.join(download_path, filename), 'wb').write(rr.content)
                                    try:
                                        mp4_video_tags = MP4(os.path.join(download_path, filename))
                                        mp4_video_tags['\xa9cmt'] = video_desc
                                        mp4_video_tags.save()
                                    except Exception as e:
                                        pass
                                    logger.info(
                                        "({:d}/{:d}) - Downloaded video with Id: {}".format(checked_total + 1,
                                                                                            available_total,
                                                                                            video_uri))
                                    downloaded_total += 1
                                else:
                                    logger.warn("Response did not return status 200, was {:d} instead. Trying with "
                                                "lower bitrate.".format(rr.status_code))
                                    rr = requests.get(Constants.VIDEO_BASE_URL.format(video_uri, 0), verify=True, headers=Constants.REQUESTS_VIDEO_UA)
                                    if rr.status_code == 200:
                                        open(os.path.join(download_path, filename), 'wb').write(rr.content)
                                        logger.info(
                                            "({:d}/{:d}) - Downloaded video with Id: {}".format(checked_total + 1,
                                                                                                available_total,
                                                                                                video_uri))
                                        downloaded_total += 1
                                    else:
                                        logger.warn("Response did not return status 200, was {:d} instead. Giving up "
                                                    "and moving on.".format(rr.status_code))
                                        logger.warn("The video Id was: {:s}".format(video_uri))
                            else:
                                logger.info("({:d}/{:d}) - Already downloaded video with Id: {}".format(checked_total + 1,
                                                                                                        available_total,
                                                                                                        video_uri))
                        checked_total += 1
                if has_more:
                    logger.separator()
                    logger.info("Retrieving next feed page (page {:d})".format(current_feed_page))
                    logger.separator()
    except KeyboardInterrupt:
        logger.separator()
        logger.info("The download has been aborted.")
        logger.separator()
    except Exception as e:
        logger.separator()
        logger.error("Something went wrong: " + str(e))
        logger.separator()


def download_single(video_id):
    try:
        download_path = os.path.join(ptts.dl_path, video_id + ".mp4")
        if not os.path.isfile(download_path):
            rr = requests.get(Constants.VIDEO_BASE_URL.format(video_id, 1), verify=True, headers=Constants.REQUESTS_VIDEO_UA)
            if rr.status_code == 200:
                open(download_path, 'wb').write(rr.content)
                logger.info("Downloaded video with Id: {}".format(video_id))
            else:
                logger.warn("Response did not return status 200, was {:d} instead. Trying with lower "
                            "bitrate.".format(rr.status_code))
                rr = requests.get(Constants.VIDEO_BASE_URL.format(video_id, 0), verify=True,  headers=Constants.REQUESTS_VIDEO_UA)
                if rr.status_code == 200:
                    open(download_path, 'wb').write(rr.content)
                else:
                    logger.warn("Response did not return status 200, was {:d} instead. Giving up.".format(rr.status_code))
            logger.separator()
        else:
            logger.binfo("This video already exists.")
            logger.separator()
    except KeyboardInterrupt:
        logger.separator()
        logger.info("The download has been aborted.")
        logger.separator()
    except Exception as e:
        logger.separator()
        logger.error("Something went wrong: " + str(e))
        logger.separator()


def download_live(target_user_id):
    if not os.path.exists(os.path.join(ptts.dl_path, ptts.tt_target_user, 'broadcasts')):
        os.makedirs(os.path.join(ptts.dl_path, ptts.tt_target_user, 'broadcasts'))

    download_path = os.path.join(ptts.dl_path, ptts.tt_target_user, 'broadcasts')
    logger.separator()
    logger.info("Checking for ongoing livestreams.")
    logger.separator()
    json_data = api.user_post_feed(user_id=target_user_id, max_cursor=0)
    if  json_data.get("aweme_list"):
        live_room_id = json_data.get("aweme_list")[0].get('author', None).get('room_id', None)
        if live_room_id:
            logger.info("Livestream available, getting information and beginning download.")
            logger.separator()
            s = requests.Session()
            s.headers.update({
                'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:60.0) Gecko/20100101 Firefox/60.0',
            })
            r = s.get(Constants.LIVE_WEB_URL.format(live_room_id))
            r.raise_for_status()
            live = r.text
            live_info_obj = re.search(r'(?<=__INIT_PROPS__ = )(.*)(?=<\/)', live)[0]
            live_info_obj = live_info_obj.replace('\\', '').replace("'", "\"").replace("false", "\"false\"")
            live_info_obj_json = json.loads(live_info_obj)
            live_hls_url = live_info_obj_json.get("/share/live/:id").get("liveData").get("LiveUrl")
            logger.info("HLS url: {:s}".format(live_hls_url))
            logger.separator()
            logger.info("HLS url retrieved. Calling youtube-dl.")
            helpers.call_ytdl(live_hls_url, os.path.join(download_path, str(live_room_id) + "_" + ptts.epochtime))
        else:
            logger.info("There is no available livestream for this user.")
            logger.separator()
    else:
        logger.info("There is no available livestream for this user.")
        logger.separator()




    ### NEEDS LOGIN BUT IS BROKEN ###

    # if not os.path.exists(os.path.join(ptts.dl_path, ptts.tt_target_user, 'broadcasts')):
    #     os.makedirs(os.path.join(ptts.dl_path, ptts.tt_target_user, 'broadcasts'))
    #
    # download_path = os.path.join(ptts.dl_path, ptts.tt_target_user, 'broadcasts')
    # logger.separator()
    # logger.info("Checking for ongoing livestreams.")
    # logger.separator()
    # json_data = api.user_post_feed(user_id=target_user_id, max_cursor=0)
    # if  json_data.get("aweme_list"):
    #     live_room_id = json_data.get("aweme_list")[0].get('author', None).get('room_id', None)
    #     if live_room_id:
    #         logger.info("Livestream available, getting information and beginning download.")
    #         logger.separator()
    #         live_json = api.get_live_feed(live_room_id)
    #         live_hls_url = Constants.LIVE_HLS_ENDP.format(live_json.get('room').get('stream_url').get('sid'))
    #         logger.info("HLS url retrieved. Calling youtube-dl.")
    #         helpers.call_ytdl(live_hls_url, os.path.join(download_path, str(live_room_id) + "_" + ptts.epochtime))
    #     else:
    #         logger.info("There is no available livestream for this user.")
    #         logger.separator()
    # else:
    #     logger.info("There is no available livestream for this user.")
    #     logger.separator()