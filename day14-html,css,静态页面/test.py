import socket

sock = socket.socket()
sock.bind(('localhost', 8001))
sock.listen(5)
while True:
    sock.accept()
