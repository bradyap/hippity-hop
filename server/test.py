import socket

HOST = "127.0.0.1"
PORT  = 9999

addr = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
msg = "hello"
sock.sendto(msg.encode(), addr)