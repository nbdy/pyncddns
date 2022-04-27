from argparse import ArgumentParser
from loguru import logger as log
from pyncddns.Updater import Updater


def main():
    ap = ArgumentParser()
    ap.add_argument("-i", "--ip", help="does not need to be set, will be fetched from the specified site")
    ap.add_argument("--host", action="append", nargs="+", help="subdomains to update")
    ap.add_argument("-d", "--domain", type=str, required=True, help="tld under which the subdomains run")
    ap.add_argument("-p", "--password", type=str, required=True, help="the dyndns password")
    ap.add_argument("-s", "--sleep-time", default=3600, type=int,
                    help="time between checking ip and updating if ip has changed")
    ap.add_argument("-v", "--verbose", action="store_true", help="be more verbose")
    ap.add_argument("--ip-site", type=str, default="https://api.ipify.org",
                    help="site on which to fetch the current ip; needs to be plain text")
    a = ap.parse_args()

    a.hosts = []
    for h in a.host:
        a.hosts.append(h[0])

    u = Updater(a)
    try:
        u.start()
        u.join()
    except KeyboardInterrupt:
        log.info("Caught CTRL + C")
        u.stop()
        u.join()

    log.info("Exiting.")


if __name__ == '__main__':
    main()
