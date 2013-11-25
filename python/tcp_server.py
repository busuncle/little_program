import socket
import time


address = ("127.0.0.1", 2012)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(address)
s.listen(1)


conn, address = s.accept()
print "connect by %s:%s" % address
try:
    while True:
        data = conn.recv(1024**3)
        if not data:
            print "sleep 0.5s"
            time.sleep(0.5)
        print data
except Exception, ex:
    print ex
    conn.close()

