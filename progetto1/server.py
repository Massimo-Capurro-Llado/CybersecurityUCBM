#!/usr/bin/env python
from http.server import BaseHTTPRequestHandler, HTTPServer


class Server(BaseHTTPRequestHandler):

	# metodo GET
	def do_GET(self):

		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		message = "Hello world!"
		self.wfile.write(bytes(message, "utf8"))
	def log_message(self, format, *args):
        	return
		
		
def run(server_class=HTTPServer, handler_class=Server, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    
  #  print ('Starting httpd on port %d...' % port)
    httpd.serve_forever()
    
if __name__ == "__main__":
    from sys import argv
    
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
