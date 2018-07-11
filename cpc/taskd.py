#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import os
import time
import signal
import logging
import psutil
import re
import subprocess

logger = logging.getLogger('task')
SCRPET = ''
NAME_NOPOSTFIX = ''
PIDFILE = ''
task_obj = task = config = _param = None


def daemon(stdout='/dev/null', stderr=None, stdin='/dev/null', pidfile=None, startmsg='started with pid %s'):
    '''''
         This forks the current process into a daemon.
         The stdin, stdout, and stderr arguments are file names that
         will be opened and be used to replace the standard file descriptors
         in sys.stdin, sys.stdout, and sys.stderr.
         These arguments are optional and default to /dev/null.
        Note that stderr is opened unbuffered, so
        if it shares a file with stdout then interleaved output
         may not appear in the order that you expect.
    '''
    # flush io
    sys.stdout.flush()
    sys.stderr.flush()
    # Do first fork.
    try:
        pid = os.fork()
        if pid > 0:
            # return first parent.
            return
    except OSError, e:
        sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)
    # Decouple from parent environment.
    #os.chdir("/")
    os.umask(0)
    os.setsid()
    # Do second fork.
    try:
        pid = os.fork()
        if pid > 0:
            # Exit second parent.
            sys.exit(0)
    except OSError, e:
        sys.stderr.write("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)

    # Open file descriptors and print start message
    if not stderr:
        stderr = stdout
    si = file(stdin, 'r')
    so = file(stdout, 'a+')
    se = file(stderr, 'a+', 0)
    pid = str(os.getpid())
    #sys.stderr.write("\n%s\n" % startmsg % pid)
    sys.stderr.flush()
    if pidfile:
        file(pidfile, 'w+').write("%s\n" % pid)
    # Redirect standard file descriptors.
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


def processinfo(x):
    x = x.strip()
    name = None
    p = psutil.get_process_list()
    for r in p:
        r = str(r)
        if re.search('pid=' + x, r):
            name = re.search("name='(.*)'", r).group(1)
    return name


def start():
    global task_obj

    pid = os.getpid()
    print "Starting", NAME_NOPOSTFIX, "..."
    if os.path.exists(PIDFILE):
        name = processinfo(open(PIDFILE).readline())
        if name and name == 'python':
            print "%s has been running PID:%s" % (SCRPET, open(PIDFILE).readline())
            return
        else:
            subprocess.call(["rm " + PIDFILE], shell=True)

    #成为daemon
    daemon(pidfile=PIDFILE)
    time.sleep(1)
    if pid == os.getpid():
        if os.path.exists(PIDFILE):
            print "Start OK", "PID:%s" % open(PIDFILE).readline()
        else:
            print "Start failed"
    else:
        #注册信号
        signal.signal(signal.SIGUSR1, signal_handler)
        signal.signal(signal.SIGUSR2, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGQUIT, signal_handler)

        try:
            task_obj = task(config, _param)
            task_obj.run()
        except Exception as e:
            logger.exception(e)


def stop():
    if os.path.exists(PIDFILE):
        pid = int(open(PIDFILE).readline().strip())
        subprocess.call(["rm " + PIDFILE], shell=True)
        os.kill(pid, signal.SIGTERM)
        print 'Stop ok'


def restart():
    stop()
    time.sleep(1)
    start()


def reload():
    pass


def signal_handler(signum, frame):
    if task_obj:
        task_obj.signal_handler(signum, frame)


def run(a, b, c):
    global SCRPET, NAME_NOPOSTFIX, PIDFILE, task_obj, task, config, _param

    task = a
    config = b
    _param = c
    HOME = os.getcwd()
    SCRPET = os.path.basename(sys.argv[0])
    if len(sys.argv) != 2 or sys.argv[1] == '-h':
        sys.exit("Usage:sudo %s ServerName {start, stop, restart, reload}" % SCRPET)

    OP = sys.argv[1]
    NAME_NOPOSTFIX = SCRPET.split(".")[0]
    PIDFILE = HOME + "/%s.pid" % NAME_NOPOSTFIX
    ops[OP]()


ops = {"start": start, "stop": stop, "restart": restart, "reload": reload}
