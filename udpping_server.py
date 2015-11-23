#!/usr/bin/env python
'''
Copyright (C) 2015 Chris Freas (code@packetbusters.net)

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
'''

import socket,random,argparse

ip = socket.gethostbyname(socket.gethostname())
port = 54321

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('',port))

parser = argparse.ArgumentParser()
parser.add_argument("-R", help="randomly drop packets", action='store_true')

args = parser.parse_args()

while True:
    data, client = s.recvfrom(1024) #client is a (ip,port) tuple
    print "received message:'" + data + "' from", client[0]
	#I just echo back what was sent by the client. Could be useful for
	#checksumming
    if args.R:
        if(random.random() > 0.5):
            s.sendto(data,client)
    else:
        s.sendto(data,client)

