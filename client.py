import socket

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = "localhost"
PORT = 5000
connection.connect((IP, PORT))
connection.send("И тебе привет!".encode('utf8'))
rd = connection.recv(1024)
print(type(rd))
print(rd.decode())
connection.close()