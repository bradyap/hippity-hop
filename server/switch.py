import socket

def bytes_to_mac(mac_bytes):
    return ':'.join(f'{b:02x}' for b in mac_bytes)

# Updates ARP table with source MAC and associated address
def update_arp(arp_table, src_mac, addr):
    if src_mac not in arp_table or arp_table[src_mac] != addr:
        arp_table[src_mac] = addr
        print(f"Updated ARP table: {arp_table}")

def main ():
    HOST = "127.0.0.1"
    PORT  = 9999

    # TODO: Command line args for addr/port

    addr = (HOST, PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(addr)

    print(f"Listening on {HOST}:{PORT}")

    arp_table = {}

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
        
        # Update ARP table
        update_arp(arp_table, src_mac, addr) # Update arp table
        
        if dest_mac == "ff:ff:ff:ff:ff:ff": # If broadcast addr, send to everyone but source
            for mac in arp_table:
                if mac != src_mac:
                    sock.sendto(data, arp_table[mac])
                    print(f"Sent packet to {mac}")
        elif dest_mac in arp_table: # Otherwise, send to specific MAC if in table
            sock.sendto(data, arp_table[dest_mac])
            print(f"Sent packet to {dest_mac}")
        else: # If we can't find destination, drop the packet
            print(f"Destination MAC {dest_mac} not found in ARP table, dropping")

if __name__=="__main__":
    main()