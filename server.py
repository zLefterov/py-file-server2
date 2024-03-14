import http.server
import socketserver
import os

PORT = 8001

class CustomHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            # Redirect to upload.html
            self.path = '/upload.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/upload':
            # The length of the data
            length = int(self.headers['content-length'])
            # The data itself (as bytes)
            data = self.rfile.read(length)

            # Process each file
            for part in data.split(b'------WebKitFormBoundary'):
                if b'Content-Disposition: form-data; name="files";' in part:
                    # Extract the filename
                    filename = part.split(b'filename="')[1].split(b'"')[0].decode()
                    file_data = part.split(b'\r\n\r\n')[1].rsplit(b'\r\n', 1)[0]

                    # Write the file
                    with open(filename, 'wb') as file:
                        file.write(file_data)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Files uploaded successfully!')

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print("Server started at:" + str(PORT))
    httpd.serve_forever()
