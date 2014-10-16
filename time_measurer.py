#!/usr/bin/env python
# -*- coding: utf-8 -*-
# запускает переданную программу со всеми переданными ключами, меряет время выполнения и шлет в графит
# !!!important  | - не обрабатывается
# 12/10/2014 Anatoly Burtsev onotole@yandex-team.ru

from __future__ import print_function
import os
import sys
import time
import subprocess as sb
import socket

GRAPHITE_HOST="localhost"
GRAPHITE_PORT=2003

if len(sys.argv) == 1: 
    exit(0)
command = sys.argv[1:]
P = sb.Popen( command, stdout=sb.PIPE, stderr=sb.PIPE )

T0 = time.time()
out, err = P.communicate()
dT = time.time() - T0 

#print(out[:-1])
if err: print(err, file=sys.stderr)

#send to graphite
MESSAGE = 'stats.test test %d %d\n' % (int(dT), int(time.time()))

#print(MESSAGE)

sock = socket.create_connection( (GRAPHITE_HOST, GRAPHITE_PORT))
sock.sendall( MESSAGE )
sock.close()
