import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 9999

def mac_to_bytes(mac_str):
    return bytes([int(x, 16) for x in mac_str.split(':')])

def bytes_to_mac(mac_bytes):
    return ':'.join(f'{b:02x}' for b in mac_bytes)

server_addr = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Usage: python3 test.py <mac_address>
mac = sys.argv[1]
print(f"mac address: {mac}")

def listen():
    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    recv_sock.bind(('0.0.0.0', 0))  # bind to any port
    print(f"listening on port {recv_sock.getsockname()[1]}")
    
    # say hello
    ethertype_bytes = bytes([0x88, 0x88])
    frame = mac_to_bytes("ff:ff:ff:ff:ff:ff") + mac_to_bytes(mac) + ethertype_bytes + b"hello everyone"
    sock.sendto(frame, server_addr)
    
    while True:
        data, addr = sock.recvfrom(1024)
        
        dest_bytes= data[0:6]
        src_bytes = data[6:12]
        ethertype_bytes = data[12:14]
        
        dest_mac = bytes_to_mac(dest_bytes)
        src_mac = bytes_to_mac(src_bytes)
        
        ethertype = f'0x{ethertype_bytes[0]:02x}{ethertype_bytes[1]:02x}' # Figure out what this is
        
        payload = data[14:] # For testing only
        str = payload.decode()
        
        print(f"Received packet from {src_mac} to {dest_mac}, ethertype: {ethertype}, payload: {str}")

# Start the receiver thread
listener = threading.Thread(target=listen, daemon=True)
listener.start()

# send messages
print("type <destination_mac> <message>")

while True:
    try:
        user_input = input("> ")
            
        parts = user_input.split(' ', 1)     
        dest_mac, payload = parts
            
        # create and send efra,e
        dest_mac_bytes = mac_to_bytes(dest_mac)
        mac_bytes = mac_to_bytes(mac)
        ethertype_bytes = bytes([0x88, 0x88])
        frame = dest_mac_bytes + mac_bytes + ethertype_bytes + payload.encode()
        sock.sendto(frame, server_addr)
        
    except KeyboardInterrupt:
        print("\nexiting...")
        break

sock.close()