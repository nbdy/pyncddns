from runnable import Runnable
from time import time, sleep
from requests import get
from loguru import logger as log


class Updater(Runnable):
    config = None
    ip = None

    def __init__(self, config):
        Runnable.__init__(self)
        self.do_run = True
        self.config = config

    def work(self):
        ip = self.get_ip()
        if self.ip is not ip:
            if self.config.verbose:
                log.info("IP changed: '{}' != '{}'", self.ip, ip)
            self.ip = ip
            for host in self.config.hosts:
                if self.config.verbose:
                    log.info("Updating: {}", host)
                self.update(self.ip, host, self.config.domain, self.config.password)
        if self.config.verbose:
            log.info("Sleeping for {} seconds.", self.config.sleep_time)
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
            log.error("Password incorrect!")
            exit()
