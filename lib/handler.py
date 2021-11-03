#!/usr/bin/python3.7
from http.server import HTTPServer, BaseHTTPRequestHandler

class DefaultHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        #self.send_response(200)
        #self.end_headers()
        #self.wfile.write(b'Hello, world!')

def start_handler(port, log, outfile):
    httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    httpd.serve_forever()
