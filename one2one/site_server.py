#!/usr/bin/env python3
import http.server
import socketserver
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = 8811

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=HERE, **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

if __name__ == '__main__':
    print(f"Serving one2one webapp on http://localhost:{PORT}/webapp/index.html")
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()




