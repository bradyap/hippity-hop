import socket

HOST = "127.0.0.1"
PORT  = 9999

addr = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def mac_to_bytes(mac_str):
    return bytes([int(x, 16) for x in mac_str.split(':')])

# test addresses
dest_mac = "00:11:22:33:44:55"
src_mac = "aa:bb:cc:dd:ee:ff"

dest_mac_bytes = mac_to_bytes(dest_mac)
src_mac_bytes = mac_to_bytes(src_mac)

# test ethertype
ethertype_bytes = bytes([0x88, 0x88])

payload = "hello testing testing 123"

frame = dest_mac_bytes + src_mac_bytes + ethertype_bytes + payload.encode()

sock.sendto(frame, addr)