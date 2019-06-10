from requests import get
from sys import argv
from time import sleep
from threading import Thread  # could use Timer but imagine how much less code that would be


class Configuration(object):
    ip = None
    hosts = []
    domain = None
    password = None
    sleep_time = 60*60
    verbose = False

    @staticmethod
    def help():
        print("usage: updater.py {arguments}")
        print("[arguments]")
        print("\t-i\t--ip")
        print("\t-h\t--host")
        print("\t-d\t--domain")
        print("\t-p\t--password")
        print("\t-s\t--sleep-time\tdefault: 3600")
        print("\t-v\t--verbose")
        print("\t--help")
        exit()

    @staticmethod
    def parse():
        cfg = Configuration()
        i = 0
        while i < len(argv):
            if argv[i] in ["-i", "--ip"]:
                cfg.ip = argv[i + 1]
            elif argv[i] in ["-h", "--host"]:
                cfg.hosts.append(argv[i + 1])
            elif argv[i] in ["-d", "--domain"]:
                cfg.domain = argv[i + 1]
            elif argv[i] in ["-p", "--password"]:
                cfg.password = argv[i + 1]
            elif argv[i] in ["-s", "--sleep-time"]:
                cfg.sleep_time = int(argv[i + 1])
            elif argv[i] in ["-v", "--verbose"]:
                cfg.verbose = True
            elif argv[i] in ["--help"]:
                Configuration.help()
            i += 1

        if len(cfg.hosts) == 0:
            print("host list is empty")
            exit()
        if cfg.domain is None:
            print("what domain should i use?")
            exit()
        if cfg.password is None:
            print("not sure if you can log in without a password")
            exit()

        return cfg


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
            sleep(self.config.sleep_time)

    def stop(self):
        self.do_run = False

    @staticmethod
    def get_ip():
        d = get("http://checkip.dyndns.com/")
        d = d.content.split(b":")[1]
        d = d.split(b"<")[0]
        d.replace(' ', '')
        return d

    @staticmethod
    def update(ip, host, domain, password):
        get('https://dynamicdns.park-your-domain.com/update', params={
            "ip": ip,
            "host": host,
            "domain": domain,
            "password": password
        })


if __name__ == '__main__':
    u = Updater(Configuration.parse())
    try:
        u.start()
    except KeyboardInterrupt:
        u.stop()
