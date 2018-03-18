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
#    print "I'm a daemon, I need root privileges. \n \n Exiting."
#    sys.exit(1)


"""
# Initialize logger subsets / locations
logger = logging.getLogger('imdaemon')
# Set lowest form of logging
logger.setLevel(logging.DEBUG)

# Setup handling to the console, again with the lowest form of logging.
log_to_console = logging.StreamHandler()
log_to_console.setLevel(logging.DEBUG)
"""
# CLI Argument Parsing


parser = argparse.ArgumentParser(description = 'This is a light weight daemon to run background processes.')
parser.add_argument('--daemonize', help='Runs this in background as a "true" daemon - uninterruptible', required = True)
parser.add_argument('-help', action='help', help="Show this help message")
parser.add_argument('--port', action='help', help="Port of which to listen on. Default will be 33884")
parser.add_argument('--stdout', help="Adds daemon processes to stdout. Off by default.")
parser.add_argument('-v', help='Increases Verbosity of the script / daemon. Look for more redirection to syslog as well.', action='store_true')
parser.add_argument('--sleeptime', help='For how long to sleep between daemonization cycles.')

args = parser.parse_args()
