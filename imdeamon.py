#!/usr/bin/python
"""daemon-Eyes

Disk And Execution MONitor

This is meant to be as pythonic as possible to illustrate daemonization
and functionality / termination within standard process state codes.

Bits and pieces taken from the watch rack for changes script as well as http://code.activestate.com/recipes/278731-creating-a-daemon-the-python-way/

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
# Default umask / file  mode creation mask of the daemon.
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
def daemonization():
    """Detach a process from the controlling terminal and run it in the background as a true daemon"""
    try:
        # Fork child process, and returns control to shell
        # This guaranteed that the child will not be a process group leader (parent)
        pid = os.fork()
    except OSError, e:
        raise Exception, "%s [%d]" % (e.strerror,e.errno)
    if (pid == 0):   # First Child Process
        os.setsid()
        """
        setsid() creates a new session if the calling process is not a process group leader.
        The calling process is the leader of the new session, the process group leader of the new process group, and
        has no controlling terminal. The process group ID and session ID of the calling process are set to the PID of the calling process.
        The calling process will be the only process in this new process group and in this new session.
        """

        try:
            # Fork a second child process, and exit immediately to prevent zombie processes.
            pid = os.fork() # Fork second child
        except OSError, e:
            raise Exception, "%s [%d]" % (e.strerror, e.errno)

        if (pid == 0):
            os.chdir(WORKDIR)
            os.umask(UMASK)

        else:
                os._exit(0) # Exit Parent (the first child) of the second child.
    else:
        print "PID is currently registering as ",pid
# CLI Argument Parsing
parser = argparse.ArgumentParser(description = 'This is a light weight daemon to demonstrate a syslog server / daemon over UDP which inherits from a syslog client.')
parser.add_argument('-help', action='help', help="Show this help message, and exit.")
parser.add_argument('--logfile', help='Path to the logfile. May not be useful when using the --verbose flag.')
parser.add_argument('-v', help='Increases Verbosity of the script / daemon. Look for more redirection to syslog as well.', action='store_true')
if len(sys.argv) < 2:
    parser.print_usage()
    #parser.print_help() # More verbose output for non args.
    sys.exit(1)
else:
    # Initialize the command-line arguments dictionary, and populate $
    #
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

daemonization()
