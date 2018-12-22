import requests
import os

try:
    import ptts
    import logger
    import api
    from constants import Constants
except ImportError:
    from . import ptts
    from . import api
    from . import logger
    from .constants import Constants


def download_all(target_user_id):
    max_cursor = 0
    has_more = 0
    downloaded_total = 0
    checked_total = 0
    available_total = 0

    if not os.path.exists(os.path.join(ptts.dl_path, ptts.tt_target_user)):
        os.makedirs(os.path.join(ptts.dl_path, ptts.tt_target_user))

    download_path = os.path.join(ptts.dl_path, ptts.tt_target_user)

    while True:
        if ptts.args.recent:
            logger.separator()
            logger.binfo("Only checking the first 10 videos (--recent was passed).")
        if not has_more and not max_cursor:
            logger.separator()
            logger.info("Retrieving first feed page...")
            logger.separator()
        json_data = api.user_post_feed(user_id=target_user_id, max_cursor=max_cursor)
        max_cursor = json_data.get('max_cursor')
        has_more = json_data.get('has_more')
        if not json_data.get("aweme_list", None):
            if downloaded_total:
                logger.separator()
                logger.info("End of feed reached. {:d} {:s} been downloaded.".format(
                    downloaded_total, "video has" if downloaded_total == 1 else "videos have"))
            else:
                logger.info("There are no available videos to download.")
            logger.separator()
            break
        else:
            available_total += len(json_data.get("aweme_list"))
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
                    if video_uri.isdigit():
                        filename = str(video.get("create_time")) + ".mp4"
                        actual_video_uri = video.get("video").get("play_addr").get("url_list")[0]
                        if not os.path.isfile(os.path.join(download_path, filename)):
                            logger.info("({:d}/{:d}) - Downloading video with Id: {}".format(checked_total + 1, available_total, video_uri))
                            rr = requests.get(actual_video_uri, verify=True,
                                              headers={"User-Agent": Constants.REQUESTS_UA["User-Agent"]})
                            open(os.path.join(download_path, filename), 'wb').write(rr.content)
                            downloaded_total += 1
                        else:
                            logger.info("({:d}/{:d}) - Already downloaded video with Id: {}".format(checked_total + 1, available_total, video_uri))
                    else:
                        video_uri = video.get("video").get("play_addr").get("uri")
                        filename = str(video.get("create_time")) + ".mp4"
                        if not os.path.isfile(os.path.join(download_path, filename)):
                            logger.info("({:d}/{:d}) - Downloading video with Id: {}".format(checked_total + 1, available_total, video_uri))
                            rr = requests.get(Constants.VIDEO_BASE_URL.format(video_uri), verify=True,
                                              headers={"User-Agent": Constants.REQUESTS_UA["User-Agent"]})
                            open(os.path.join(download_path, filename), 'wb').write(rr.content)
                            downloaded_total += 1
                        else:
                            logger.info("({:d}/{:d}) - Already downloaded video with Id: {}".format(checked_total + 1, available_total, video_uri))
                    checked_total += 1
            if has_more:
                logger.separator()
                logger.info("Retrieving next feed page...")
                logger.separator()