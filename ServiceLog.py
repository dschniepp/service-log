#!/usr/bin/env python

import urlparse, sys, os,urlparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from subprocess import call

class ServiceLog(BaseHTTPRequestHandler):

    quiet = False
    daemon = False

    def do_GET(self):
        if self.path == '/start':
            call("start-stop-daemon --exec servicelog.sh --background --start", shell=True)
        if self.path == '/stop':
            call("start-stop-daemon --exec servicelog.sh --background --stop", shell=True)

def main():
    try:
        server = None
        for arg in sys.argv: 
            if(arg == '-d' or arg == '--daemon-mode'):
                ServiceLog.daemon = True
                ServiceLog.quiet = True
            if(arg == '-q' or arg == '--quiet'):
                ServiceLog.quiet = True
                
        if(ServiceLog.daemon):
            pid = os.fork()
            if(pid != 0):
                sys.exit()
            os.setsid()

        if(not ServiceLog.quiet):
            print 'ServiceLog Service v 0.1 started'
        else:
            print 'ServiceLog Service v 0.1 started in daemon mode'
             
        server = HTTPServer(('', 8080), ServiceLog)
        server.serve_forever()
    except (KeyboardInterrupt, SystemExit) as e:
        if(e): # wtf, why is this creating a new line?
            print >> sys.stderr, e

        if(not server is None):
            server.socket.close()

        if(not ServiceLog.quiet):
            print 'Goodbye'

if __name__ == '__main__':
     main()
