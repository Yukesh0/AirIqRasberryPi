#!/usr/bin/env python3
"""
AirIQ PMS5003 Web Dashboard Server
Simple HTTP server for real-time air quality monitoring with SQLite storage
"""
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import json
import os
import urllib.parse
import time
import mimetypes
import sys
import random
from datetime import datetime

from db import insert_reading, get_latest_reading, get_history_24h, get_all_records

ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(ROOT, 'templates')

class DashboardHandler(BaseHTTPRequestHandler):
    """HTTP request handler for dashboard and API endpoints"""

    def send_json(self, obj, status=200):
        """Send JSON response"""
        data = json.dumps(obj).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(data)

    def serve_file(self, fullpath):
        """Serve static file"""
        if not os.path.exists(fullpath) or not os.path.isfile(fullpath):
            self.send_error(404)
            return
        ctype = mimetypes.guess_type(fullpath)[0] or 'application/octet-stream'
        with open(fullpath, 'rb') as f:
            data = f.read()
        self.send_response(200)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        """Handle GET requests"""
        parsed = urllib.parse.urlparse(self.path)
        p = parsed.path

        # Serve main dashboard
        if p in ('/', '/index.html'):
            full = os.path.join(TEMPLATES, 'index.html')
            return self.serve_file(full)

        # Serve static files
        if p.startswith('/static/'):
            full = os.path.join(ROOT, p.lstrip('/'))
            return self.serve_file(full)

        # Serve logo files
        if p.startswith('/logo/'):
            full = os.path.join(ROOT, p.lstrip('/'))
            return self.serve_file(full)

        # API: Current sensor data
        if p == '/api/data':
            # Generate random sensor reading
            pm1 = 2.5 + random.uniform(-0.5, 1.0)
            pm25 = 10 + random.uniform(-2, 5)
            pm10 = 16 + random.uniform(-3, 8)
            
            # Save to database
            insert_reading(pm1, pm25, pm10)
            
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            obj = {
                'connected': True,
                'pm1': pm1,
                'pm25': pm25,
                'pm10': pm10,
                'timestamp': now
            }
            print(f"[{now}] Saved: PM1.0={pm1:.1f}, PM2.5={pm25:.1f}, PM10={pm10:.1f}")
            return self.send_json(obj)

        # API: Historical data for chart
        if p == '/api/history':
            # Generate random sensor reading
            pm1 = 2.5 + random.uniform(-0.5, 1.0)
            pm25 = 10 + random.uniform(-2, 5)
            pm10 = 16 + random.uniform(-3, 8)
            
            # Save to database first
            insert_reading(pm1, pm25, pm10)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Saved: PM1.0={pm1:.1f}, PM2.5={pm25:.1f}, PM10={pm10:.1f}")
            
            # Get 24h history from database
            history = get_history_24h()
            
            obj = {
                'current': {
                    'pm1': pm1,
                    'pm25': pm25,
                    'pm10': pm10,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                'history': history
            }
            
            return self.send_json(obj)

        # API: All database records
        if p == '/api/db/all':
            records = get_all_records()
            return self.send_json({'records': records})

        # Try to serve other files
        local = os.path.join(ROOT, p.lstrip('/'))
        if os.path.exists(local) and os.path.isfile(local):
            return self.serve_file(local)

        self.send_error(404, 'Not Found')

    def log_message(self, format, *args):
        """Suppress default logging"""
        pass


def run(port=8000):
    """Start the server"""
    server = ThreadingHTTPServer(('0.0.0.0', port), DashboardHandler)
    print(f"✓ AirIQ Dashboard running at http://localhost:{port}")
    print(f"✓ Press Ctrl-C to stop\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n✓ Server stopped')
        server.shutdown()


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run(port)
