#!/usr/bin/env python3
import http.server
import json
import os

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class PRDHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        data = json.loads(body)

        if self.path == '/save':
            filename = data.get('filename', '')
            html = data.get('html', '')
            if not filename or '..' in filename or '/' in filename:
                self.send_error(400, 'Invalid filename')
                return
            filepath = os.path.join(DIRECTORY, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            self._json_ok()

        elif self.path == '/save-notes':
            filename = data.get('filename', '')
            notes = data.get('notes', {})
            if not filename or '..' in filename or '/' in filename or not filename.endswith('.json'):
                self.send_error(400, 'Invalid filename')
                return
            filepath = os.path.join(DIRECTORY, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(notes, f, ensure_ascii=False, indent=2)
            self._json_ok()

        else:
            self.send_error(404)

    def _json_ok(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'ok': True}).encode())

if __name__ == '__main__':
    with http.server.HTTPServer(('', PORT), PRDHandler) as httpd:
        print(f'PRD Server running at http://localhost:{PORT}/')
        httpd.serve_forever()
