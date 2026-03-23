import http.server
import socketserver
import webbrowser
import os

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("\n" + "="*60)
print("SmartHire.AI - Local Server")
print("="*60)
print(f"Server running at: http://localhost:{PORT}")
print("="*60)
print("\nOpen your browser to: http://localhost:8000/SmartHire_Demo.html")
print("\nPress Ctrl+C to stop the server")
print("="*60 + "\n")

# Auto-open browser
webbrowser.open(f'http://localhost:{PORT}/SmartHire_Demo.html')

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
