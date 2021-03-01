import http.server
import socketserver
import argparse
from urllib.parse import urlparse

parser = argparse.ArgumentParser(description="Sets up a small web server that redirects every GET request it gets to a different location")

parser.add_argument("target", help="The target of the redirect")
parser.add_argument("-r", "--relative", help="Treats target as relative to the domain used for the request", action="store_true")
parser.add_argument("-f", "--forward", type=int, default=None, help="Forwards the request to a different port in relative mode")
parser.add_argument("-o", "--protocol", help="Forwards to a different protocol in relative mode", default="http")
parser.add_argument("-p", "--port", type=int, default=80, help="The port on which the server will run")
parser.add_argument("-v", "--verbose", help="Outputs information each time it gets a request", action="store_true")

args = parser.parse_args()

class RedirectHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        host = self.headers.get('Host')
        self.send_response(301)
        if(args.relative):
            hostonly = host.split(':')[0]
            redTo = f"{args.protocol}://{hostonly}{f':{args.forward}' if args.forward is not None else ''}{'' if args.target.startswith('/') else '/'}{args.target}"
        else:
            redTo = args.target
        self.send_header('Location', redTo)
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Connection', 'close')
        self.end_headers()
        if(args.verbose):
            print(f"Received GET request from client {self.client_address} to host {self.headers.get('host')}, path {self.path}")
            print(f"Redirecting it to {redTo}")

port = args.port
server = socketserver.TCPServer(("", port), RedirectHandler)

print(f"Server started on port {port}")
server.serve_forever()