#! python
import requests
from time import sleep, time
from subprocess import call, DEVNULL
import logging
from systemd.journal import JournaldLogHandler

logger = logging.getLogger(__name__)
journald_handler = JournaldLogHandler()
journald_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(message)s'
))
logger.addHandler(journald_handler)
logger.setLevel(logging.DEBUG)


def login(username, password):
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
        r = requests.post(login_route, data, headers=headers)
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
    username, password = None, None
    ping_host = "1.1.1.1"
    conf_file = "/home/srinskit/.nitkcaa.conf"
    try:
        with open(conf_file, "r") as f:
            lines = [val.strip() for val in f.readlines()]
            username, password = lines[0], lines[1]
    except:
        logger.error("Could not read config file")

    long_sleep = 16
    short_sleep = 4
    while True:
        ic = is_connected(ping_host)
        if ic:
            # logger.info("connected")
            sleep(long_sleep)
        else:
            # logger.info("not connected")
            login(username, password)
            sleep(short_sleep)


if __name__ == '__main__':
    main()
