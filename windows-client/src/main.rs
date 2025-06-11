use std::net::UdpSocket;
use std::env;
use std::str::FromStr;
use mac_address::MacAddress;

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

    // testing args
    let port = String::from("9999");
    let server = String::from("127.0.0.1");

    let address = format!("{}:{}", server, port);

    println!("Attempting to connect to: {}", address);

    // set up tes tpacket
    let dest_mac = MacAddress::from_str("00:11:22:33:44:55").unwrap();
    let src_mac = MacAddress::from_str("aa:bb:cc:dd:ee:ff").unwrap();
    let ethertype = [0x08, 0x00];
    let payload = b"The sun is shining";

    // build packet
    let mut packet = Vec::new();
    packet.extend_from_slice(&dest_mac.bytes());
    packet.extend_from_slice(&src_mac.bytes());
    packet.extend_from_slice(&ethertype);
    packet.extend_from_slice(payload);

    // connect and send data
    match UdpSocket::bind("127.0.0.1:0") {
        Ok(socket) => {
            // send data to the server
            match socket.send_to(&packet, &address) {
                Ok(_) => println!("Sent Hello!"),
                Err(e) => println!("Failed to send data: {}", e),
            }
        }
        Err(e) => {
            eprintln!("Failed to bind UDP socket: {}", e);
        }
    }
}