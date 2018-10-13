#!/usr/bin/env python3

"""
# daemon-Eyes

# Becomes a daemon (think about what is involved in becoming a true daemon)
# > The first thing to think about is how to actually detach/daemonize.
# > Just a fork() isn't enough, since when the parent which has fork()'ed goes away,
# > The "daemon" ends up a zombie. Instead, it is necessary to double-fork.
# > Read up on it here, just to understand a bit more, since the note says to give it some deeper thought:
# > http://www.win.tue.nl/~aeb/linux/lk/lk-10.html

TODO:

* Logging

* Signal Handling -15 and SIGHUP -15 / SIGTERM

* PID FILE tracking - Make sure daemonizer only runs once. 

* Time based loop 
Just a reminder - this is tested with ssh

"""

import argparse
import json
import logging
import os
import resource
import sys
import time


### CLI Argument Parsing ###
parser = argparse.ArgumentParser(description = 'This is a light weight daemon to demonstrate system processing and daemonization.')
parser.add_argument('-help', action='help', help="Show this help message, and exit.")
parser.add_argument('--json', help='Specify this flag to dump output of JSON notated daemon information into the logfile as well.', required=False,action='store_true')
parser.add_argument('--verbose', help='Make the daemon more chatty.', required=False,action='store_true')
parser.add_argument('--logfile', help='Path to the logfile. If empty, output is STDOUT/STDERR, which implies something else handling logfile(s). Typically useful with --verbose')


###  Initialize logger object, with a definitive name ###
logger = logging.getLogger('DaemonLogging')
# Set "lowest" level of logging
logger.setLevel(logging.DEBUG)
# Setup handling output to the console, and set the "lowest" logging level
log_to_console = logging.StreamHandler()
log_to_console.setLevel(logging.DEBUG)

# Setup formatting of the logging. 

if args.verbose:
  formatter = logging.Formatter('%(levelname)s - %(processName)s[%(threadName)s|%(funcName)s] - %(message)s')
else:
  formatter = logging.Formatter('%(levelname)s - %(message)s')
#
# Set the console output format.
#
log_to_console.setFormatter(formatter)

# Initialize the command-line arguments dictionary, and populate it from what was parsed out.
args = parser.parse_args()

if args.logfile():
    log_to_file = 


# # Log variables
# #
# #
# LOGDIR = "/tmp/pydaemon"
# LOGFILE = LOGDIR + args.logfile
# LOGCONFIG_FILE = "/tmp/pydaemon/imdaemon-logcfg.json"
# #
# #
# #

### File Descriptor variables and the like ###

# Default umask / file  mode creation mask of the daemon.
UMASK = 0
# Working Directory
WORKDIR = "/tmp"
# Maximum File Descriptors
MAXFD = 1024    

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
            os.system("ps "),pid
        except OSError:
            print "OS System call failed for fork pid -> %d" % pid

        if (pid == 0): # Second Child. The current directory will likely be a mounted filesystem / accessible directory. 
            try:
                os.chdir(LOGDIR)
            except OSError:
                print "Unable to parse directory. Creating---"
                os.mkdir(LOGDIR)
                if os.path.exists(LOGDIR):
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
    
    return 0

def jsonDump(logFile):
    os.chdir(LOGDIR)
    fileOpen = open(logFile,'w')
    if type(fileOpen) == file: #Successfully opened logfile
        json.dump(procParams,logFile,indent=6, sort_keys = True)
        
    
    

        
    # with open(args.logfile,'w') as jsonoutfile)
    #     json.dump(procParams,jsonoutfile)
    
    
    # json.dumps(args.logfile,indent=6, sort_keys = True)
    # return 0

if __name__ == "__main__":
    
    if args.json:
        print "json Argument received"
        jsonDump(args.logfile)

    retCode = daemonization()
    procParams = """
    return code = %s
    process ID = %s
    parent process ID = %s
    process group ID = %s
    session ID = %s
    user ID = %s
    effective user ID = %s
    real group ID = %s
    effective group ID = %s
    """ % (retCode, os.getpid(), os.getppid(), os.getpgrp(), os.getsid(0),os.getuid(),os.geteuid(),os.getgid(),os.getegid())
    daemonLog = open(args.logfile,"w").write(procParams + "\n")
   
    


    
    daemonization()
