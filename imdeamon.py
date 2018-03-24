#!/usr/bin/python
"""Steve Homick
2018
imdaemon.py
"""
import argparse
import logging
import os
import sys
import time

if os.geteuid() != 0:
    print "I'm a daemon, I need root / sudo. \n \n Exiting."
    sys.exit(1)

# Default umask creation
UMASK = 0

# Default working dir
WORKDIR = "/tmp"

# Maximum File Descriptors
MAXFD = 1024

# I/O File Descriptors are sent to /dev/null by default.
if (hasattr(os, "devnull")):
    REDIRECT_TO = os.devnull
else:
    REDIRECT_TO = "/dev/null"
# Begin daemonization
def createDaemon():
    try:
        # Fork child process so the parent can exit successfully.
        # Failed call to fork raises exception(s)
        pid = os.fork()
        pidofFork = os.getpid()
    except OSError, e:
        raise Exception, "%s [%d]" % (e.strerror, e.errno)
    if (pid == 0): # First child process
        os.setsid()

"""
watchrack example logging

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
parser.add_argument('-v', help='Increases Verbosity of the script / daemon. Look for more redirection to syslog as well.', action='store_true')


args = parser.parse_args()

# Set basic logging config.
LOG_FILE = ""
logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='', filename=LOG_FILE, filemode = 'a')
