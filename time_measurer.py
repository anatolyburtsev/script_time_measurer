#!/usr/bin/env python
# -*- coding: utf-8 -*-
# запускает переданную программу со всеми переданными ключами, меряет время выполнения и шлет в графит
# !!!important  | - не обрабатывается
# 12/10/2014 Anatoly Burtsev onotole@yandex-team.ru

#TODO read GRAPHITE_HOST and PORT from config

from __future__ import print_function
import os
import sys
import time
import subprocess as sb
import socket
import re

GRAPHITE_HOST = "localhost"
GRAPHITE_PORT = 2003
HOST = socket.gethostname().split('.')[0]

if len(sys.argv) == 1: 
    exit(0)
command = sys.argv[1:]
SCRIPT = sys.argv[1]
# skip "/usr/bin/flock -w 0 /tmp/.flock_tmp" 
# may be need improve
if SCRIPT == "/usr/bin/flock":
    SCRIPT = sys.argv[5]
#/usr/bin/gdb -> gdb
SCRIPT=SCRIPT.split('/')[-1]
P = sb.Popen( command, stdout=sb.PIPE, stderr=sb.PIPE )

T0 = time.time()
out, err = P.communicate()
dT = time.time() - T0

out=out.encode()
err=err.encode()
#remove magic additional newline
if out != "": print(out[:-1])
if err != "": print(err[:-1], file=sys.stderr)

#send to graphite
MESSAGE = 'stats.timemeasurer.%s.%s %d %d\n' % (HOST, SCRIPT, int(dT), int(time.time()))

#print(MESSAGE)

sock = socket.create_connection( (GRAPHITE_HOST, GRAPHITE_PORT))
sock.sendall( MESSAGE )
sock.close()
