use std::net::UdpSocket;
use std::env;

fn main() {

    // accept cmd line arguments
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        eprintln!("Usage: cargo run <server> <port>");
        std::process::exit(1);
    }

    // set up connection args
    // let server = &args[1];
    // let port = &args[2];

    // testing args
    let port = String::from("9999");
    let server = String::from("127.0.0.1");

    let address = format!("{}:{}", server, port);

    println!("Attempting to connect to: {}", address);

    // connect and send data
    match UdpSocket::bind("127.0.0.1:0") {
        Ok(socket) => {
            // send data to the server
            match socket.send_to(b"hello", &address) {
                Ok(_) => println!("Sent Hello!"),
                Err(e) => println!("Failed to send data: {}", e),
            }
        }
        Err(e) => {
            eprintln!("Failed to bind UDP socket: {}", e);
        }
    }
}