import socket
from sys import argv
from threading import Thread, Lock


def connection_manager_thread(addr, conn):
	while True:
		data = conn.recv(1024)
		if not data:
			break
		conn.sendall(data)
	conn.close()
     
           
localIP = '192.168.0.7'
port = int(argv[1])

# Create socket with the port received as cmd argument                          
TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
TCPServerSocket.bind((localIP, port))

# Start socket managed by a thread 	
while True:
	TCPServerSocket.listen()
	conn, addr = TCPServerSocket.accept()
	Thread(target=connection_manager_thread, args=(addr, conn),).start()
	
TCPServerSocket.close()

