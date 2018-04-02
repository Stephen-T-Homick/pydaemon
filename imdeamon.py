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

"""
Upon completion, deploy.

if os.geteuid() != 0:
    print "I'm a daemon, I need root / sudo. \n \n Exiting."
    sys.exit(1)
    """
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
def main():
    try:
        if args.logfile:
            log_to_file = logging.FileHandler(args,logfile)
            log_to_file.setLevel(logging.DEBUG)
            log_to_file.setFormatter(formatter)
            logger.addHandler(log_to_file)
            logger.info("startup")
        else:
            logger.addHandler(log_to_console)
            logger.debug("Startup")

    except IOError as e:
        logger.critical("Error trying to open {} error({}): {}".format(args.logfile,e.errno,e.strerror))
# CLI Argument Parsing
parser = argparse.ArgumentParser(description = 'This is a light weight daemon to demonstrate a syslog server / daemon over UDP which inherits from a syslog client.')
parser.add_argument('-help', action='help', help="Show this help message, and exit.")
parser.add_argument('--logfile', help='Path to the logfile. May not be useful when using the --verbose flag.')
parser.add_argument('-v', help='Increases Verbosity of the script / daemon. Look for more redirection to syslog as well.', action='store_true')
args = parser.parse_args()

# Set basic logging config.
LOG_FILE = ""
logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='', filename=LOG_FILE, filemode = 'a')

#
#  Initialize logger object, with a definitive name
#
logger = logging.getLogger('logDaemon')
# Set "lowest" level of logging
logger.setLevel(logging.DEBUG)
# Setup handling output to the console, and set the "lowest" logging level
log_to_console = logging.StreamHandler()
log_to_console.setLevel(logging.DEBUG)

#
# Set the default format of the logger
#
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#
# Set the console output format.
#
log_to_console.setFormatter(formatter)

main()
