#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/if.h>
#include <linux/if_tun.h>

int init_tap(char *devname) {
    struct ifreq ifr; // Interface request structure
    int fd, err;

    // Open device
    fd = open("/dev/net/tun", O_RDWR);
    if (fd < 0) {
        perror("Failed to open /dev/net/tun");
        return -1;
    }

    //memset(&ifr, 0, sizeof(ifr));
    ifr.ifr_flags = IFF_TAP | IFF_NO_PI; // Tap mode without extra header infront of eframe
    strncpy(ifr.ifr_name, devname, IFNAMSIZ); // Set device name

    // Create and return tap interface
    ioctl(fd, TUNSETIFF, &ifr);
    return fd;
}

int main() {
    char name[] = "tap0";
    int tap_fd = init_tap(name);
    if (tap_fd < 0) {
        perror("Couldn't initialize tap interface");
        return 1;
    }
    printf("Tap interface %s initialized successfully\n", name);

    // Connect to server and send hello message
    

    // Handle ethernet frames
    unsigned char buffer[2048];
    while (1) {
        int n = read(tap_fd, buffer, sizeof(buffer));
        //if (n < 0) break;
        printf("Received %d bytes\n", n);
    }

    close(tap_fd);
    return 0;
}

// Write Ethernet frame to TAP
//write(tap_fd, ethernet_frame, frame_len);

// Read incoming frames
//read(tap_fd, buffer, sizeof(buffer));