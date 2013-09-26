import re
import sys


if len(sys.argv) < 2:
    print "not file!"
    exit(0)

patterns = [
    r"(?P<name>Windows) (?P<version>.+?)[;\)\n]",
    r"(?P<name>Android)[/ ](?P<version>\d+\.\d+)",
    r"OS (?P<version>[\d_]+?) like (?P<name>Mac OS X)",
    r"(?P<name>Mac OS X) (?P<version>[\d_]+?)", 
    r"(?P<name>Windows)(?P<version>)",
    r"(?P<name>Android)(?P<version>)",
    r"(?P<name>Mac OS X)(?P<version>)", 
    r"(?P<name>Linux)(?P<version>)",
]

res = {}
others = []
with open(sys.argv[1]) as fp:
    for line in fp:
        os, version = "others", "others"
        for pat in patterns:
            s = re.search(pat, line)
            if s is not None:
                os, version = s.group("name"), s.group("version")
                if os == "Mac OS X":
                    version = version.split("_")[0]
                if len(version) == 0:
                    version = "others"
                break

        res[os, version] = res.get((os, version), 0) + 1
        if os == "others":
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

