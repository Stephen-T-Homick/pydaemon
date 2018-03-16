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
import time








# Initialize logger subsets / locations
logger = logging.getLogger('imdaemon')


# CLI Argument Parsing

parser = argparse.ArgumentParser()
parser.add_argument('--pidfile', help='.', required = True)
parser.add_argument('--verbose', help='Increases Verbosity of the script / daemon. Look for more redirection to syslog as well.', action='store_true')
parser.add_argument('--host', help='Remote host against which to run. Default: netbox.datto.net')
parser.add_argument('--sleeptime', help='For how long to sleep between loops')