#!/usr/bin/python3

from requests import get
from time import sleep, time
from threading import Thread  # could use Timer but imagine how much less code that would be
from argparse import ArgumentParser


class Updater(Thread):
    do_run = False
    config = None
    ip = None

    def __init__(self, config):
        Thread.__init__(self)
        self.do_run = True
        self.config = config

    def run(self):
        while self.do_run:
            ip = self.get_ip()
            if self.ip is not ip:
                if self.config.verbose:
                    print(self.ip, "!=", ip)
                self.ip = ip
                for host in self.config.hosts:
                    if self.config.verbose:
                        print("updating", host)
                    self.update(self.ip, host, self.config.domain, self.config.password)
            if self.config.verbose:
                print("sleeping for", self.config.sleep_time, "seconds")
            self.sleep_cycle()

    def sleep_cycle(self):
        ss = time()
        while (time() - ss) < self.config.sleep_time:
            if not self.do_run:
                break
            sleep(1)

    def stop(self):
        self.do_run = False

    def get_ip(self):
        return get(self.config.ip_site).content

    @staticmethod
    def update(ip, host, domain, password):
        r = get('https://dynamicdns.park-your-domain.com/update', params={
            "ip": ip,
            "host": host,
            "domain": domain,
            "password": password
        })
        if "Passwords do not match" in r.text:
            print("password incorrect")
            exit()


if __name__ == '__main__':
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
        print("\ncaught ctrl+c; stopping")
        u.stop()
