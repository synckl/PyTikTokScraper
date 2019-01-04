import argparse
import configparser
import logging
import os
import sys
import json

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
        elif args.getfollowing:
            ptts.tt_target_user = args.getfollowing
        elif args.livestream:
            ptts.tt_target_user = args.livestream
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
                        help="The username (or uid) of the user whose posts you want to save.")
    parser.add_argument('-r', '--recent', dest='recent', action='store_true',
                        help="When used, only retrieves the first 10 videos in the user's feed.")
    parser.add_argument('-gf', '--get-following', dest='getfollowing', type=str, required=False,
                        help="When used, retrieves the list of people you're following.")
    parser.add_argument('-uid', '--is-uid', dest='isuid', action='store_true',
                        help="When used, treat the download argument as the user ID.")
    parser.add_argument('-s', '--single', dest='single', type=str, required=False,
                        help="Pass a single video Id to download.")
    parser.add_argument('-l', '--livestream', dest='livestream', type=str, required=False,
                        help="Pass an username to download a livestream, if available.")
    args = parser.parse_args()

    if validate_inputs(config, args):
        api.login(username=ptts.tt_username, password=ptts.tt_password)
        if ptts.tt_active_user:
            logger.info("Login successful.")
            logger.separator()
            logger.info("Getting user information for '{:s}'.".format(ptts.tt_target_user))
            if not args.isuid:
                try:
                    target_user_json = api.search_user(ptts.tt_target_user)
                    target_user_id = target_user_json.get('user_list')[0].get('user_info').get('uid')
                except IndexError as e:
                    logger.separator()
                    logger.error("No user found matching '{:s}', the script will now exit.".format(ptts.tt_target_user))
                    logger.separator()
                    sys.exit(1)
            else:
                target_user_id = args.download
            if target_user_id:
                logger.separator()
                logger.info("Retrieved user ID: {:s}".format(target_user_id))
                logger.separator()
            else:
                logger.separator()
                logger.warn("No user ID found. Exiting.")
                logger.separator()
                sys.exit(1)
            if args.getfollowing:
                logger.info("Retrieving list of following users...")
                logger.warn("Pagination does not work properly, use this at own risk!")
                logger.separator()
                json_resp = api.get_following(target_user_id)
                following_txt = os.path.join(os.getcwd(), "following_{:s}.txt".format(ptts.tt_target_user))
                if os.path.isfile(following_txt):
                    os.remove(following_txt)
                for user in json_resp.get('followings'):
                    user_text = user.get('unique_id') + " - " + user.get('uid')
                    logger.plain(user_text)
                    open(following_txt, 'a').write(user_text + '\n')
                logger.separator()
                logger.info("Written {:d} users to {:s}".format(len(json_resp.get('followings')), following_txt))
                logger.separator()
            if ptts.args.download:
                logger.info("Starting download of all videos from profile.")
                downloader.download_all(target_user_id)
            elif ptts.args.single:
                logger.info("Starting download of single video by id.")
                downloader.download_single(ptts.tt_target_id)
            elif ptts.args.livestream:
                logger.info("Starting download for livestream.")
                downloader.download_live(target_user_id)
