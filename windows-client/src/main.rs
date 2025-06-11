use mac_address::MacAddress;
use std::net::UdpSocket;
use std::str::FromStr;
use std::{env, error::Error, thread};
use std::io::{self, Write};

fn main() {
    // accept cmd line arguments
    // let args: Vec<String> = env::args().collect();
    // if args.len() != 3 {
    //     eprintln!("Usage: cargo run <server> <port>");
    //     std::process::exit(1);
    // }

    // set up connection args
    // let server = &args[1];
    // let port = &args[2];

    // cmdline to set client's MAC addr
    let args: Vec<String> = env::args().collect();
    let src_mac = &args[1];

    // testing args
    let port = String::from("9999");
    let server = String::from("127.0.0.1");

    let address = format!("{}:{}", server, port);

    println!("Attempting to connect to: {}", address);

    // set up packet
    let dest_mac = String::from("ff:ff:ff:ff:ff:ff");
    // let src_mac = String::from("aa:bb:cc:dd:ee:ff");
    let ethertype = [0x08, 0x00];
    let payload = b"The sun is shining";

    let packet = build_ethernet_packet(&dest_mac, &src_mac, &ethertype, payload).expect("Failed to build ");

    // bind for listening
    let socket = UdpSocket::bind("127.0.0.1:0").expect("Could not bind");

    // send initial packet
    socket.send_to(&packet, &address).expect("Failed to send initial packet");

    // set up thread to handle incoming requests
    let in_socket = socket.try_clone().expect("Failed to clone socket");
    let addr_clone = address.clone();

    thread::spawn(move || {
        let mut buf = [0;1024];
        loop {
            match in_socket.recv_from(&mut buf) {
                Ok((n, src)) => {
                    println!("Received {} bytes from {}", n, src);

                    let in_payload = &buf[14..n];
                    match std::str::from_utf8(in_payload) {
                        Ok(s) => println!("Payload: {}", s),
                        Err(_) => println!("Payload (non-UTF8): {:?}", payload),
                    }
                    print!("^-^ -> ");
                    io::stdout().flush().unwrap();
                }
                Err(e) => {
                    eprintln!("Error receiving: {}", e);
                    break;
                }
            }
        }
    });

    // main loop handling messages
    loop {
        print!("^-^ -> ");
        io::stdout().flush().unwrap();
        let mut input = String::new();
        io::stdin().read_line(&mut input).expect("Failed to read input");

        let new_payload = input.trim().as_bytes();
        let packet = build_ethernet_packet(&dest_mac, &src_mac, &ethertype, new_payload).unwrap();
        socket.send_to(&packet, &addr_clone).unwrap();
    }

}

fn build_ethernet_packet(
    dest_mac: &str,
    src_mac: &str,
    ethertype: &[u8],
    payload: &[u8],
) -> Result<Vec<u8>, Box<dyn Error>> {
    let dest = MacAddress::from_str(dest_mac)?.bytes();
    let src = MacAddress::from_str(src_mac)?.bytes();

    let mut packet = Vec::with_capacity(dest.len() + src.len() + ethertype.len() + payload.len());

    packet.extend_from_slice(&dest);
    packet.extend_from_slice(&src);
    packet.extend_from_slice(ethertype);
    packet.extend_from_slice(payload);

    Ok(packet)
}
