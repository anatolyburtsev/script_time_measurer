#!/usr/bin/env python
# -*- coding: utf-8 -*-
# запускает переданную программу со всеми переданными ключами, меряет время выполнения и шлет в графит
# !!!important  | - не обрабатывается
# 12/10/2014 Anatoly Burtsev onotole@yandex-team.ru
#TODO read GRAPHITE_HOST and PORT from config

import os
import sys
import time
import subprocess as sb
import socket

GRAPHITE_HOST = "localhost"
GRAPHITE_PORT = 2003
HOST = socket.gethostname().split('.')[0]

if len(sys.argv) == 1: 
    exit(0)
command = sys.argv[1:]

script_name_position=1
# skip "/usr/bin/flock -w 0 /tmp/.flock_tmp" 
# may be need improve
if sys.argv[script_name_position] == "/usr/bin/flock":
    script_name_position = 5

SCRIPT = sys.argv[script_name_position]

#/usr/bin/gdb -> gdb
SCRIPT=SCRIPT.split('/')[-1]

#special for differ "get_smth.py thing1" and "get_smth.py thing2"
if len(sys.argv[script_name_position:]) >= 2 and sys.argv[script_name_position+1][0] not in '0123456789-': 
    SCRIPT = SCRIPT + '_' + sys.argv[script_name_position+1]

#delele extenstion
SCRIPT = SCRIPT.replace('.sh','').replace('.py','')

P = sb.Popen( command, stdout=sb.PIPE, stderr=sb.PIPE )

T0 = time.time()
out, err = P.communicate()
dT = time.time() - T0

sys.stdout.write(out)
sys.stderr.write(err)

#send to graphite
MESSAGE = 'stats.timemeasurer.%s.%s %d %d\n' % (HOST, SCRIPT, int(dT), int(time.time()))

#print(MESSAGE)

sock = socket.create_connection( (GRAPHITE_HOST, GRAPHITE_PORT))
sock.sendall( MESSAGE )
sock.close()
