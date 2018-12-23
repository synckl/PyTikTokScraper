import argparse
import configparser
import logging
import os

try:
    import ptts
    import logger
    import api
    import downloader
    from constants import Constants
except ImportError:
    from . import ptts
    from . import api
    from . import logger
    from . import downloader
    from .constants import Constants


def validate_inputs(config, args):
    error_arr = []
    try:
        config.read(os.path.join(os.getcwd(), "settings.ini"))
        logger.banner()

        ptts.tt_username = config.get('ptts', 'username')
        ptts.tt_password = config.get('ptts', 'password')
        ptts.dl_path = config.get('ptts', 'download_path')
        ptts.args = args

        if not ptts.tt_username or not len(ptts.tt_username):
            raise Exception("Invalid value for 'username'. This value is required.")

        if not ptts.tt_password or not len(ptts.tt_password):
            raise Exception("Invalid value for 'password'. This value is required.")

        if not ptts.dl_path.endswith('/'):
            ptts.dl_path = ptts.dl_path + '/'
        if not ptts.dl_path or not os.path.exists(ptts.dl_path):
            ptts.dl_path = os.getcwd()
            error_arr.append(["dl_path", ptts.dl_path])

        if error_arr:
            for error in error_arr:
                logger.warn("Invalid value for '{:s}'. Using default value: {:s}".format(error[0], error[1]))
                logger.separator()

        if args.download:
            ptts.tt_target_user = args.download
        elif args.single:
            ptts.tt_target_id = args.single
        else:
            logger.error("Missing --download or --single argument. Either of these arguments is required.")
            logger.separator()
            return False

        return True
    except Exception as e:
        logger.error("An error occurred: {:s}".format(str(e)))
        logger.error("Make sure the config file and given arguments valid and try again.")
        logger.separator()
        return False


def run():
    ptts.initialize()
    logging.disable(logging.CRITICAL)
    config = configparser.ConfigParser()
    parser = argparse.ArgumentParser(
        description="You are running PyTikTokScraper {:s} using Python {:s}".format(Constants.SCRIPT_VER,
                                                                                    Constants.PYTHON_VER))
    parser.add_argument('-d', '--download', dest='download', type=str, required=False,
                        help="The username of the user whose posts you want to save.")
    parser.add_argument('-r', '--recent', dest='recent', action='store_true',
                        help="When used, only retrieves the first 10 videos in the user's feed.")
    parser.add_argument('-s', '--single', dest='single', type=str, required=False,
                        help="Pass a single video Id to download.")
    args = parser.parse_args()

    if validate_inputs(config, args):
        api.login(username=ptts.tt_username, password=ptts.tt_password)
        if ptts.tt_active_user:
            if ptts.tt_target_user:
                logger.info("Login successful.")
                logger.separator()
                logger.info("Getting user information for '{:s}'.".format(ptts.tt_target_user))

                target_user_json = api.search_user(ptts.tt_target_user)
                target_user_id = target_user_json.get('user_list')[0].get('user_info').get('uid')

                logger.separator()
                logger.info("Retrieved user ID: {:s}".format(target_user_id))
                logger.separator()
                logger.info("Starting download of all videos from profile.")
                downloader.download_all(target_user_id)
            elif ptts.tt_target_id:
                logger.info("Downloading single video by id. No authentication required.")
                downloader.download_single(ptts.tt_target_id)