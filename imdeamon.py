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
import resource
import sys
import time
try:
    import resource

except ImportError:
    print "\n 'resource' library not available. Install with `pip install resource`, skipping for now \n"

# Logger variables
#
#
LOGDIR = "/var/log/pydaemon"
LOGFILE = "/var/log/pydaemon/imdaemon.log"
LOGCONFIG_FILE = "/var/log/pydaemon/imdaemon-logcfg.json"
#
#

# Default umask / file  mode creation mask of the daemon.
UMASK = 0

# Working Directory
WORKDIR = "/tmp"
# Maximum File Descriptors
MAXFD = 1024

# Logger object Setup, with definitive name.
logger = logging.getLogger('daemonicLogger')

# Set 'lowest' level of logging by default. 
logger.setLevel(logging.DEBUG)

    


# I/O File Descriptors are sent to /dev/null by default.
if hasattr(os, "devnull") == True:
    REDIRECT_TO = os.devnull

else:
    REDIRECT_TO = "/dev/null"

# Begin daemonization
def daemonization():
    """Detach a process from the controlling terminal and run it in the background as a true daemon"""
    try:
        # Fork child process, and returns control to shell
        # This guaranteed that the child will not be a process group leader (parent)
        if hasattr(os,"fork"):
            pid = os.fork()
    except OSError, e:
        raise Exception, "%s [%d]" % (e.strerror,e.errno)   

    if (pid == 0):   # First Child Process, session leader.
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
        except OSError:
            print "OS System call failed for fork pid -> %d" % pid

        if (pid == 0): # Second Child. The current directory will likely be a mounted filesystem / accessible directory. 
            os.chdir(WORKDIR)
            os.umask(UMASK)

        else:
                os._exit(0) # Exit Parent (the first child) of the second child.
    else:
        print "PID is currently registering as ",pid
        os._exit(0)
# Close all open file descriptors ^ 
    maxfd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]


    if (maxfd == resource.RLIM_INFINITY):
        maxfd = MAXFD # Sets maxfd back to 1024

        # Iterator to close all file descriptors.
    for fd in range(0,maxfd):
        try:
            os.close(fd)
        except OSError: # If file descriptor was not open from the start.
            pass
    # Redirect standard I/O file descriptors to the specified file. Most file descriptors are sent to /dev/null to avoid conflictions. 
    os.open(REDIRECT_TO, os.O_RDWR) #Standard input (0)

    # Duplicate standard input to standard output and standard error.
    os.dup2(0,1) # Duplicate file descriptor. - Standard output (1)
    os.dup2(0,2) # Standard error (2)
    
# CLI Argument Parsing
parser = argparse.ArgumentParser(description = 'This is a light weight daemon to demonstrate system processing and daemonization.')
parser.add_argument('-help', action='help', help="Show this help message, and exit.")
parser.add_argument('--logfile', help='Manual naming convention of log file. Default name / path is /var/log/pydaemon/imdaemon.log', required=False)
parser.add_argument('--verbose', help='Increases verbosity of the script / daemon, raises criticality of logging / debugging', action='store_true')

args = parser.parse_args()

if args.verbose:
    logger.setLevel(logging.CRITICAL)

else:

    daemonization()
