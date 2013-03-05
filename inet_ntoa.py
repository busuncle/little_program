import socket
import struct

def inet_ntoa(n):
    """
    complicated in using inet_ntoa in python for some consideration
    like this: ip = socket.inet_ntoa(struct.pack(">L", n))
    make it easy
    """
    assert 0 <= n < 2**32 - 1
    res = []
    mask = 2**8 - 1
    for i in xrange(4):
        t = n & mask
        res.insert(0, t)
        n >>= 8

    return ".".join(map(str, res))


if __name__ == "__main__":
    n = 3449552015
    print socket.inet_ntoa(struct.pack(">L", n))
    print inet_ntoa(n)

