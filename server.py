from __future__ import annotations

from socketserver import BaseRequestHandler, ThreadingMixIn, TCPServer
import pickle
import queue
import threading

from server_commands import CommandHandler, CommandNotFoundException


tasks_db: dict[str, CommandHandler] = {}  # id : command_handler
tasks_queue: queue.Queue = queue.Queue()

def run_commands():
    while True:
        try:
            command = tasks_queue.get(timeout=1)
        except queue.Empty:
            pass
        else:
            command.process_data()


class TCPHandler(BaseRequestHandler):

    def handle(self):
        raw_data = self.request.recv(4096)
        try:
            data = pickle.loads(raw_data)
        except EOFError:
            return
        action = data[0]

        if action == "start":
            _, command_name, data = data
            try:
                command_handler = CommandHandler(data, command_name)
            except CommandNotFoundException as e:
                response = str(e).encode("utf-8")
            else:
                tasks_db[command_handler.id] = command_handler
                tasks_queue.put(command_handler)
                response = command_handler.get_encoded_id()

        elif action == "status":
            command_handler = tasks_db.get(data[1])
            if command_handler:
                response = command_handler.get_encoded_status()
            else:
                response = "Несуществующий task_id".encode("utf-8")

        elif action == "response":
            command_handler = tasks_db.get(data[1])
            if command_handler:
                response = command_handler.get_encoded_response()
            else:
                response = "Несуществующий task_id".encode("utf-8")

        self.request.sendall(response)

class ThreadedTCPServer(ThreadingMixIn, TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    host = "localhost"
    port = 5000

    with ThreadedTCPServer((host, port), TCPHandler) as srv:
        threading.Thread(target=run_commands, daemon=True).start()
        srv.serve_forever()
