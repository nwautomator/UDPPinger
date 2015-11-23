#!/usr/bin/env python
'''
Copyright (C) 2015 Chris Freas (code@packetbusters.net)

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

NOTE: Python 2.7 or newer is needed. Python 3 not supported!
'''

import socket,IN,time,sys,errno

# No standard deviation function in the Python 2.x standard library. Ugh.
def standard_deviation(numbers):
    average = (sum(numbers))/len(numbers)
    variance = [(p - average)**2 for p in numbers]
    stddev = [(p)**0.5 for p in variance]
    stddev = (sum(stddev))/len(stddev)
    return stddev

# Some needed variables
sent_pkts = 0
rcvd_pkts = 0
stats = []
timeout = 1
reuse_socket = 0
packet_count = 10
payload = "hello!"
source_port = 54322
dest_port = 54321
target = None

# Program options - these are the setsockopt() options as required for
# graduate students. See lines 46 and 49 below.
def parse_args(args):
    # this is kludgy, but neither argparse nor getopt allow for free-form arguments 
    # like this.
    global reuse_socket, interface, packet_count, payload, dest_port, source_port,\
            timeout, target
    usage =  "usage: " + args[0] + " [-R] [-I <interface>] [-c count] [-h] [-p <payload>] [-P dst port] [-S src port] [-t timeout] destination\n-R\treuse socket\n-I foo\tuse interface 'foo' when sending packets\n-c x\tsend x packets to destination\n-h\tdisplay this help\n-p foo\tspecify a payload\n-P x\t the destination port to probe\n-S x\tthe source port to bind to\n-t x\tresponse timeout in seconds (default is 1 second)\ndestination\tthe destination host or IP to probe"

    if len(args) < 2:
        print usage
        sys.exit(0)
    if "-h" in args:
        print usage
        sys.exit(0)
    if "-R" in args:
        # this is the SO_REUSEADDR socket option
        reuse_socket = 1
    if "-I" in args:
        # this is the SO_BINDTODEVICE socket option
        interface = args[args.index("-I") + 1] + '\0'
    if "-c" in args:
       packet_count = int(args[args.index("-c") + 1])
    if "-p" in args:
       payload = args[args.index("-p") + 1] 
       if len(payload) == 0:
           print "Payload can't be null!"
           sys.exit(1)
    if "-P" in args:
       dest_port = int(args[args.index("-P") + 1])
    if "-S" in args:
       source_port = int(args[args.index("-S") + 1])
    if "-t" in args:
       timeout = int(args[args.index("-t") + 1])
    target = args[-1]

parse_args(sys.argv)
if target is None:
    parse_args([sys.argv[0]])
    sys.exit(1)

target_ip = socket.gethostbyname(target)

# Set up the socket and bind it
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(float(timeout))
s.bind(('',source_port)) #I'm not binding to any particular IP

# set the socket options to the user defined values
if "-R" in sys.argv:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, reuse_socket)
if "-I" in sys.argv:
    try:
        s.setsockopt(socket.SOL_SOCKET, IN.SO_BINDTODEVICE, interface)
    except socket.error as serror:
        if serror.errno == errno.EPERM:
            print "Need root permissions to do this"
            sys.exit(1)
        if serror.errno == errno.ENODEV:
            print "That interface does not exist!"
            sys.exit(1)
        print "Unknown error:" + serror
        sys.exit(1)


if timeout != 1:
    print "UDP PING " + target + ", timeout set to " + str(timeout) + " seconds"
else:
    print "UDP PING " + target

for x in range(packet_count):
    try:
        s.sendto(payload, (target_ip,dest_port))
        sent_pkts += 1
        stime = time.time()
        data, junk = s.recvfrom(1024)
        etime = time.time()
        rcvd_pkts += 1
        rtt = 1000*(etime - stime) # in milliseconds
        stats.append(rtt)
        print str(sys.getsizeof(data)) + " bytes from " + target_ip + " seq=" + str(x) + " time=%5.3f" % rtt + " ms"
    except socket.timeout:
        print "Request timeout for seq " + str(x)
    except socket.error as e:
        if e.errno == errno.EINVAL:
            parse_args([sys.argv[0]])
        print "Error sending packet: %s" %str(e)

print "\n--- " + target + " UDP ping statistics ---"
print str(sent_pkts) + " packets transmitted, " + str(rcvd_pkts) + " received, " + str(100*(1-(float(rcvd_pkts)/float(sent_pkts)))) + "% packet loss" 

if len(stats) > 1:
    print "round-trip min/avg/max/stddev = %5.3f/%5.3f/%5.3f/%5.3f" %(min(stats),(sum(stats))/len(stats), max(stats), standard_deviation(stats)) + " ms"

#we're done!
s.close()
