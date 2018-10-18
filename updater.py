from requests import get
from sys import argv
from time import sleep
from threading import Thread


def parse_args():
    cfg = {
        "ip": None,
        "host": None,
        "domain": None,
        "password": None,
        "sleep_time": 60*60
    }
    i = 0
    while i < len(argv):
        if argv[i] in ['-h', '--help']:
            print cfg.keys()
            exit()
        elif argv[i] in ["-i", "--ip"]:
            cfg["ip"] = argv[i + 1]
        elif argv[i] in ["-h", "--host"]:
            cfg["host"] = argv[i + 1]
        elif argv[i] in ["-d", "--domain"]:
            cfg["domain"] = argv[i + 1]
        elif argv[i] in ["-p", "--password"]:
            cfg["password"] = argv[i + 1]
        elif argv[i] in ["-s", "--sleep-time"]:
            cfg["sleep_time"] = int(argv[i + 1])
        i += 1
    return cfg


class Updater(Thread):
    do_run = False
    password = None
    domain = None
    host = None
    sleep_time = None
    ip = None

    def __init__(self, **kwargs):
        Thread.__init__(self)
        self.do_run = True
        _ = kwargs.keys()
        if "password" in _:
            self.password = kwargs.get("password")
        elif "domain" in _:
            self.domain = kwargs.get("domain")
        elif "host" in _:
            self.host = kwargs.get("host")
        elif "sleep_time" in _:
            self.sleep_time = kwargs.get("sleep_time")

        for _ in [self.password, self.domain, self.host, self.sleep_time]:
            if _ is None:
                self.do_run = False

    def run(self):
        while self.do_run:
            ip = self.get_ip()
            if self.ip is not ip:
                self.ip = ip
                self.update(self.ip, self.host, self.domain, self.password)
            sleep(self.sleep_time)

    def start(self):
        self.run()

    def stop(self):
        self.do_run = False

    @staticmethod
    def get_ip():
        d = get("http://checkip.dyndns.com/")
        d = d.content.split(':')[1]
        d.replace(" ", "")
        d = d.split("<")[0]
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
    u = Updater(kwargs=parse_args())
    try:
        u.start()
    except KeyboardInterrupt:
        u.stop()
