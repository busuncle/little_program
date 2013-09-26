import re
import sys


if len(sys.argv) < 2:
    print "no input file!"
    exit(0)


patterns = [
    r"(?P<name>MSIE) (?P<version>\d+?)\D", 
    r"(?P<name>Chrome)/(?P<version>\d+?)\D", 
    r"(?P<name>Firefox)/(?P<version>\d+?)\D", 
    r"Version/(?P<version>\d+?)\D.+ (?P<name>Safari)", 
    r"(?P<name>Opera)/(?P<version>\d+?)\D",

    r"(?P<name>MSIE)(?P<version>)",
    r"(?P<name>Chrome)(?P<version>)",
    r"(?P<name>Firefox)(?P<version>)",
    r"(?P<name>Safari)(?P<version>)",
    r"(?P<name>Opera)(?P<version>)",

    r"(?P<name>Maxthon)[/ ](?P<version>\d+?)\D",
    r"(?P<name>UCBrowser)[/ ](?P<version>\d+?)\D",
    r"(?P<name>MQQBrowser)[/ ](?P<version>\d+?)\D",
]


res = {}
others = []
with open(sys.argv[1]) as fp:
    for line in fp:
        browser, version = "others", "others"
        for pat in patterns:
            s = re.search(pat, line)
            if s is not None:
                browser, version = s.group("name"), s.group("version")
                if len(version) == 0:
                    version = "others"
                break

        res[browser, version] = res.get((browser, version), 0) + 1
        if browser == "others":
            others.append(line)


def cmp_func(a, b):
    if a[0] < b[0]:
        return -1
    elif a[0] == b[0]:
        if a[1].isdigit() and b[1].isdigit():
            return -1 if int(a[1]) <= int(b[1]) else 1
        else:
            return -1 if a[1] <= b[1] else 1
    else:
        return 1


for k, v in sorted(res.iteritems(), cmp=cmp_func, key=lambda (k, v): k):
    print k, v

#for v in others:
#    print v
#print "others sum: %s" % len(others)
