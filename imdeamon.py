#!/usr/bin/python
"""Steve Homick 2018
https://github.com/Stephen-T-Homick
 Daemon written from scratch
 http://www.linfo.org/daemon.html
 'A daemon is a type of program on Unix-like operating systems that runs unobtrusively in the background,
 rather than under the direct control of a user, waiting to be activated by the occurance of a specific event or condition.''
"""

import argparse
import logging
import socket
import sys
import time


# CLI Argument Parsing

parser = argparse.ArgumentParser()
parser.add_argument('--daemonize', help='Runs this in background as a "true" daemon - uninterruptible', required = True)
parser.add_argument('-v', help='Increases Verbosity of the script / daemon. Look for more redirection to syslog as well.', action='store_true')
parser.add_argument('--sleeptime', help='For how long to sleep between daemonization cycles.')

# Initialize logger subsets / locations
logger = logging.getLogger('imdaemon')
# Set lowest form of logging
logger.setLevel(logging.DEBUG)

# Setup handling to the console, again with the lowest form of logging.
log_to_console = logging.StreamHandler()
log_to_console.setLevel(logging.DEBUG)
