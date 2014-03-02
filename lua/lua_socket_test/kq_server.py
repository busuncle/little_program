#!/usr/bin/python
# -*- coding:utf8 -*-
import socket, select
from datetime import datetime


READ_MAX = 1024
KQ_TIMEOUT = 5
SOCKET_LISTEN = 10

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 1234))
sock.listen(SOCKET_LISTEN)
sock.setblocking(0)

kq = select.kqueue()
kq.control([select.kevent(sock, select.KQ_FILTER_READ, select.KQ_EV_ADD)], 0)

print "kq server start"

try:
    connections = {}
    while True:
        #print "kqueue main loop running"
        events = kq.control(None , 30, KQ_TIMEOUT)
        if not events:
            continue

        for event in events:
            if event.ident == sock.fileno():
                conn, address = sock.accept()
                conn.setblocking(0)
                connections[conn.fileno()] = conn
                kq.control([
                    select.kevent(conn, select.KQ_FILTER_READ, select.KQ_EV_ADD),
                ], 0)
                print "%s connected at %s, fd %s" % (address, datetime.now(), conn.fileno())

            elif event.filter == select.KQ_FILTER_READ:
                buf = connections[event.ident].recv(READ_MAX)
                if len(buf.strip()) > 0:
                    print "%s says %s" % (event.ident, buf)
                    kq.control([
                        select.kevent(event.ident, select.KQ_FILTER_WRITE, select.KQ_EV_ADD),
                    ], 0)

            elif event.filter == select.KQ_FILTER_WRITE:
                connections[event.ident].send("fuck you %s\n" % event.ident)
                kq.control([
                    select.kevent(event.ident, select.KQ_FILTER_WRITE, select.KQ_EV_DELETE),
                ], 0)

finally:
    kq.close()
    sock.close()
