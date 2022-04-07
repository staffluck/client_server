from socketserver import BaseRequestHandler, ThreadingMixIn, TCPServer

class TCPHandler(BaseRequestHandler):

    def handle(self):
        while True:
            data = self.request.recv(4096)
            self.request.sendall(data)

class ThreadedTCPServer(ThreadingMixIn, TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    host = "localhost"
    port = 5000

    with ThreadedTCPServer((host, port), TCPHandler) as srv:
        srv.serve_forever()
