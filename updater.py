from requests import get
from sys import argv
from time import sleep
from threading import Thread  # could use Timer but imagine how much less code that would be


class ConfigFieldNotFilled(Exception):
    def __init__(self, what):
        self.message = "please supply " + what + " or use --help"


def _help():
    print "usage: updater.py [arguments]"
    print "[arguments]"
    print "\t-i\t--ip"
    print "\t-h\t--host"
    print "\t-d\t--domain"
    print "\t-p\t--password"
    print "\t-s\t--sleep-time\tdefault: 3600"
    print "\t-v\t--verbose"
    print "\t--help"
    exit()


def parse_args():
    cfg = {
        "ip": None,
        "hosts": [],
        "domain": None,
        "password": None,
        "sleep_time": 60*60,
        "verbose": False
    }
    i = 0
    while i < len(argv):
        if argv[i] in ["-i", "--ip"]:
            cfg["ip"] = argv[i + 1]
        elif argv[i] in ["-h", "--host"]:
            cfg["hosts"].append(argv[i + 1])
        elif argv[i] in ["-d", "--domain"]:
            cfg["domain"] = argv[i + 1]
        elif argv[i] in ["-p", "--password"]:
            cfg["password"] = argv[i + 1]
        elif argv[i] in ["-s", "--sleep-time"]:
            cfg["sleep_time"] = int(argv[i + 1])
        elif argv[i] in ["-v", "--verbose"]:
            cfg["verbose"] = True
        elif argv[i] in ["--help"]:
            _help()
        i += 1

    for k, v in cfg.iteritems():
        if v is None:
            raise ConfigFieldNotFilled(k)

    return cfg


class Updater(Thread):
    do_run = False
    password = None
    domain = None
    hosts = None
    sleep_time = None
    ip = None
    verbose = False

    def __init__(self, domain, hosts, password, ip=None, sleep_time=60*60, verbose=False):
        Thread.__init__(self)
        self.do_run = True
        self.domain = domain
        self.hosts = hosts
        self.password = password
        self.ip = ip
        self.sleep_time = sleep_time
        self.verbose = verbose

        for _ in [self.domain, self.hosts, self.password, self.sleep_time]:
            if _ is None:
                self.do_run = False
                if self.verbose:
                    print "something has not been filled"

    def run(self):
        while self.do_run:
            ip = self.get_ip()
            if self.ip is not ip:
                if self.verbose:
                    print self.ip, "!=", ip
                self.ip = ip
                for host in self.hosts:
                    if self.verbose:
                        print "updating", host
                    self.update(self.ip, host, self.domain, self.password)
            if self.verbose:
                print "sleeping for", self.sleep_time, "seconds"
            sleep(self.sleep_time)

    def start(self):
        self.run()

    def stop(self):
        self.do_run = False

    @staticmethod
    def get_ip():
        d = get("http://checkip.dyndns.com/")
        d = d.content.split(':')[1]
        d = d.split("<")[0]
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
    c = parse_args()
    u = Updater(c["domain"], c["hosts"], c["password"], c["ip"], c["sleep_time"], c["verbose"])
    try:
        u.start()
    except KeyboardInterrupt:
        u.stop()
