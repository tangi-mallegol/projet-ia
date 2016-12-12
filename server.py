#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import json
from os import curdir, sep

PORT_NUMBER = 8080

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
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
                self.send_response(200)
                self.send_header('Content-type', "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({ "reponse" : "test" }))
        except Exception as err:
            #self.send_error(500, "Une erreur serveur s'est produite'")
            self.send_error(500, err)

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
	