#! python3
import requests
from time import sleep, time
from subprocess import call, DEVNULL
import logging
import sys
import argparse
from pathlib import Path

logging.basicConfig()
logger = logging.getLogger(__name__)

def login(username, password):
    logger.debug("Attempting login in")
    login_route = "https://nac.nitk.ac.in:8090/login.xml"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        "DNT": "1",
        "Host": "nac.nitk.ac.in:8090",
        "Origin": "https://nac.nitk.ac.in:8090",
        "Referer": "https://nac.nitk.ac.in:8090/",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    }
    data = {
        "mode": "191",
        "username": username,
        "password": password,
        "producttype": 0,
        "a": int(round(time() * 1000)),
    }
    try:
        r = requests.post(login_route, data, headers=headers,timeout=4)
        return r.ok
    except:
        pass
    return False


def is_connected(ping_host):
    try:
        ret = call(["ping", "-c1", ping_host], stdout=DEVNULL, stderr=DEVNULL)
        return ret == 0
    except:
        pass
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "config_file",
        nargs='?',
        help="Path to config file (usually ~/.nitkcaa.conf)",
        default=Path.joinpath(Path.home(), ".nitkcaa.conf")
    )
    parser.add_argument(
        "--service",
        help="run in service mode",
        action="store_true"
    )
    parser.add_argument(
        "--verbose",
        help="view more logs",
        action="store_true"
    )
    args = parser.parse_args()
    # Set root logger level to get messages from deps too
    logging.getLogger().setLevel(level=logging.DEBUG if args.verbose else logging.INFO)
    logger.info("Starting")

    username, password = None, None
    ping_host = None
    try:
        with open(args.config_file, "r") as f:
            lines = [val.strip() for val in f.readlines()]
            username, password = lines[0], lines[1]
            ping_host = lines[2]
    except:
        logger.error("Could not read config file. Check file and format")
        return

    if not args.service:
        if login(username, password):
            logger.info("Done")
        else:
            logger.error("Failed")
        return

    long_sleep = 16
    short_sleep = 4
    try:
        while True:
            logger.debug("Checking internet connectivity")
            ic = is_connected(ping_host)
            if ic:
                logger.debug("Connected to internet")
                sleep(long_sleep)
            else:
                logger.debug("Not connected to internet")
                login(username, password)
                sleep(short_sleep)
    except:
        logger.info("Shutting down")


if __name__ == '__main__':
    main()
