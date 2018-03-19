x Becomes a daemon (what does it mean for something to become a *real* daemon?)

x Do not use `systemd`, `nohup`, or similar

x Do not use a daemonizing library

x Logs clearly what is going on at every step of the process

x Allows only one instance of itself to run at a given time (and ponder about how things 
may break)

x Exits cleanly on signal (with a proper log message)


https://www.loggly.com/blog/new-style-daemons-python/
http://www.win.tue.nl/~aeb/linux/lk/lk-10.html
