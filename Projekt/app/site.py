#!/usr/bin/env python2
# coding: utf-8

import sys
import main
import web

def setup_signal_handling():
    import os
    import signal

    def kill_self(*args):
        os.kill(os.getpid(), signal.SIGKILL)

    signal.signal(signal.SIGINT, kill_self)

if __name__ == u'__main__':
    if len(sys.argv) < 2 or sys.argv[1] != u'-t':
        web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)

    else:
        sys.argv = [x for x in sys.argv if x != u'-t']
        setup_signal_handling()

    main.app.run()
