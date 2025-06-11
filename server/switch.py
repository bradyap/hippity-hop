import socket

HOST = "127.0.0.1"
PORT  = 9999

# TODO: Command line args for addr/port

addr = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(addr)

print(f"Listening on {HOST}:{PORT}")

while True:
    data, addr = sock.recvfrom(1024)
    
    if not data:
        break
    
    print(f"Received {data.decode()} from {addr}")