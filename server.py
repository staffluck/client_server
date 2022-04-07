from __future__ import annotations

from socketserver import BaseRequestHandler, ThreadingMixIn, TCPServer
import pickle
import queue
import threading

from setuptools import Command

from server_commands import CommandHandler


tasks_db: dict[str, Command] = {}  # id : command_handler

q = queue.Queue()

class TCPHandler(BaseRequestHandler):

    def handle(self):
        raw_data = self.request.recv(4096)
        try:
            data = pickle.loads(raw_data)
        except:
            data = raw_data.decode()

        if isinstance(data, list):
            command_id, data = data
            try:
                command_handler = CommandHandler(data, int(command_id))
            except Exception:
                response = "Неизвестная команда".encode("utf-8")
            else:
                tasks_db[command_handler.id] = command_handler
                response = pickle.dumps(list(tasks_db.keys()))
        else:
            command_handler = tasks_db.get(data)
            if command_handler:
                response = command_handler.get_encoded_status()
            else:
                response = "Несуществующий task_id".encode("utf-8")
        self.request.sendall(response)

class ThreadedTCPServer(ThreadingMixIn, TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    host = "localhost"
    port = 5000

    with ThreadedTCPServer((host, port), TCPHandler) as srv:
        srv.serve_forever()
