#!/usr/bin/python
# Steve Homick 2018
# Daemonizer written from scratch
# http://www.linfo.org/daemon.html
# A daemon is a type of program on Unix-like operating systems that runs unobtrusively in the background,
# rather than under the direct control of a user, waiting to be activated by the occurance of a specific event or condition.

import argparse
import logging
import socket
import sys
from time import sleep





# Initialize logger subsets / locations
logger = logging.getLogger('imdaemon')
logger.setLevel(logging,DEBUG)

# Log to console
log_to_console = logging.StreamHandler()
log_to_console.setLevel(logging.DEBUG)

# CLI Argument Parsing

parser = argparse.ArgumentParser()
parser.add_argument('--daemonize', help='Runs this in background as a "true" daemon - uninterruptible', required = True)
parser.add_argument('-v', help='Increases Verbosity of the script / daemon. Look for more redirection to syslog as well.', action='store_true')
parser.add_argument('--sleeptime', help='For how long to sleep between daemonization cycles.')
