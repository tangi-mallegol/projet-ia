#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
import urllib
import sys, traceback
from os import curdir, sep

import IVHM

PORT_NUMBER = 8080

# This class will handles any incoming request from
# the browser


class myHandler(BaseHTTPRequestHandler):

    # Handler for the GET requests
    def do_GET(self):
        try:
            url = self.path.split("?")[0]
            self.log_message(url)
            if url == "/" or url == "/index.html":
                f = open(curdir + sep + "/index.html")
                self.send_response(200)
                self.send_header('Content-type', "text/html")
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            elif url == "/question":
                uuid = 0
                try:
                    params = urllib.unquote_plus(self.path.split("question=")[1]).decode('utf8')
                    params = params.split("&uuid=")
                    query = params[0]
                    uuid = params[1]
                except:
                    traceback.print_exc(file=sys.stdout)
                    query = urllib.unquote_plus(self.path.split("question=")[1]).decode('utf8')
                res = IVHM.build_client_res(uuid, query)
                self.send_response(200)
                self.send_header('Content-type', "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"reponse": res}))
        except Exception as err:
            # self.send_error(500, "Une erreur serveur s'est produite'")
            self.send_error(500, err)


try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ', PORT_NUMBER

    # Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()
