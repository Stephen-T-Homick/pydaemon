#!/usr/bin/python
"""Steve Homick
2018
imdaemon.py"""
import argparse
import json
import logging
import os
import socket
import sys
import time

#if os.geteuid() != 0:
#    print "I'm a daemon, I need root / sudo dude. \n \n Exiting."
#    sys.exit(1)

syslogSuccessCodes = ['']

# Set basic logging config.

logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='', filename=LOG_FILE, filemode = 'a')

class SyslogUDPHandler(SocketServer.BaseRequestHandler):

    def handle_request(self):
        date = bytes.decode(self.request[0].strip())



"""
Pavel - watchrack example

# Initialize logger subsets / locations
logger = logging.getLogger('imdaemon')
# Set lowest form of logging
logger.setLevel(logging.DEBUG)

# Setup handling to the console, again with the lowest form of logging.
log_to_console = logging.StreamHandler()
log_to_console.setLevel(logging.DEBUG)
"""
# CLI Argument Parsing
parser = argparse.ArgumentParser(description = 'This is a light weight daemon to demonstrate a syslog server / daemon over UDP which inherits from a syslog client.')
parser.add_argument('--daemonize', help='Runs this in background as a "true" syslog daemon - uninterruptible.', required = False)
parser.add_argument('-help', action='help', help="Show this help message, and exit.")
parser.add_argument('--port', help='Port of which to listen on. Default will be UDP 514 (rsyslog) unless otherwise specified.', required = False)
parser.add_argument('--stdout', help="Adds daemon processes to stdout. Off by default.")
parser.add_argument('-v', help='Increases Verbosity of the script / daemon. Look for more redirection to syslog as well.', action='store_true')
parser.add_argument('--sleep', help='For how long to sleep between daemonization cycles. Example - python imdeamon.py --sleep 5m')
parser.add_argument('--zombie', help='Become zombie process')


args = parser.parse_args()
