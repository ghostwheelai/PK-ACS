# -*- coding: utf-8 -*-

import BaseHTTPServer
import CGIHTTPServer
import signal
import requests
from os import curdir, sep

#from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

server_address = ("192.168.1.63", 80)

page_head = """<html><head>
                   <title>СКУД РП</title>
                   <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
               </head><body>"""
page_tail = "</body></html>"

#class HttpProcessor(BaseHTTPServer.BaseHTTPRequestHandler):

class HttpProcessor(CGIHTTPServer.CGIHTTPRequestHandler):

    cgi_directories = [ "/cgi-bin", "/cgi"] 

    def do_GET(self):

        try:
            
            if not self.path == "/cgi/app.py":

                
            #    f = open(curdir + sep + "index.html")
            #    self.send_response(200)
            #    self.send_header("Content-Type", "text/html")
            #    self.end_headers()
            #    self.wfile.write(f.read())
            #    f.close()

            # elif self.path == "/app.py":
                self.send_response(301)
                self.send_header("Location", "/cgi/app.py")
                self.end_headers()
            else:
                if self.is_cgi():
                    self.run_cgi()
                else:
                    self.send_error(501, "Error")
            #else:
            #    self.send_response(200)
            #    self.send_header("Content-Type","text/html")
            #    self.end_headers()
            #    self.wfile.write(page_head )
            #    self.wfile.write("<center><b>Привет, Мир!</b></center>")
            #   self.wfile.write(page_tail)
        except IOError:
            self.send_error(404,"File Not Found: %s" % self.path)

httpd = BaseHTTPServer.HTTPServer(server_address, HttpProcessor)
httpd.serve_forever()

def end_read(signal,frame):

    global httpd
    httpd.server_close()

    print "Выключаем сервер"

signal.signal(signal.SIGINT, end_read)