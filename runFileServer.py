from http.server import BaseHTTPRequestHandler, HTTPServer

def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', 7001)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run()
