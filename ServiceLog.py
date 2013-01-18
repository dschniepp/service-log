#!/usr/bin/env python

import urlparse, sys, os,urlparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from subprocess import call
from os import curdir, sep

class ServiceLog(BaseHTTPRequestHandler):

    quiet = False
    daemon = False

    def do_GET(self):
        if self.path == '/start':
            call("start-stop-daemon --start --oknodo --user daniel --name servicelog -v --make-pidfile --pidfile /home/daniel/service-log/service-log.pid --exec /home/daniel/service-log/servicelog &", shell=True)

        if self.path == '/stop':
            call("start-stop-daemon --stop --oknodo --pidfile /home/daniel/service-log/service-log.pid", shell=True)
            f = open("/home/daniel/service-log/log.csv")
            self.send_response(200)
            self.send_header('Content-type',    'text/text')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()


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
             
        server = HTTPServer(('', 8001), ServiceLog)
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
