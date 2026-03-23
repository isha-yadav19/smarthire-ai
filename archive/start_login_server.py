"""
Simple HTTP Server for Login Page
Serves the auth folder on http://localhost:8000
"""

import http.server
import socketserver
import os
from pathlib import Path

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        # Redirect root to login.html
        if self.path == '/' or self.path == '/index.html':
            self.path = '/login.html'
        return super().do_GET()

# Change to auth directory
auth_dir = Path(__file__).parent / 'auth'
os.chdir(auth_dir)

print("=" * 60)
print("SmartHire.AI - Login Page Server")
print("=" * 60)
print(f"Serving from: {auth_dir}")
print(f"Server running on: http://localhost:{PORT}")
print(f"")
print(f"Open in browser:")
print(f"  -> http://localhost:{PORT}")
print(f"  -> http://localhost:{PORT}/login.html")
print("=" * 60)
print("Press CTRL+C to stop")
print()

Handler = MyHTTPRequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
