import socket
import time


address = ("127.0.0.1", 2012)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(address)
s.listen(1)


conn, address = s.accept()
conn.setblocking(0)
print "connect by %s:%s" % address
try:
    while True:
        data = None
        try:
            data = conn.recv(1024**3)
        except socket.error, ex:
            print "no data, sleep 1s"
            time.sleep(1)

        if data:
            print data

except Exception, ex:
    print ex
    conn.close()

