import socket

HOST = "127.0.0.1"
PORT  = 9999

# TODO: command line args for addr/port

addr = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(addr)

print(f"Listening on {HOST}:{PORT}")

while True:
    data, addr = sock.recvfrom(1024)
    
    dest_bytes= data[0:6]
    src_bytes = data[6:12]
    ethertype_bytes = data[12:14]
    
    dest_mac = ':'.join(f'{b:02x}' for b in dest_bytes)
    src_mac = ':'.join(f'{b:02x}' for b in src_bytes)
    
    ethertype = f'0x{ethertype_bytes[0]:02x}{ethertype_bytes[1]:02x}' # figure out what this is
    
    payload = data[14:] # for testing only
    str = payload.decode()
    
    print(f"Received packet from {src_mac} to {dest_mac}, ethertype: {ethertype}, payload: {str}")