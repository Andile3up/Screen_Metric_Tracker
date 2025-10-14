#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <termios.h>
#include <string.h>
#include <time.h>

#define SERIAL_PORT "/dev/ttyUSB0"
#define BAUD_RATE B115200

#define SERIAL_PORT2 "/dev/ttyUSB0"
#define BAUD_RATE2 B115200

// Function to get the current date and time in YYYY-MM-DD HH:MM:SS format
void get_current_datetime(char *datetime_str, size_t size) {
    time_t now = time(NULL);
    struct tm *tm_info = localtime(&now);
    strftime(datetime_str, size, "%Y-%m-%d %H:%M:%S", tm_info);
}

// Function to initialize serial port
int init_serial(const char *port) {
    int fd = open(port, O_RDWR | O_NOCTTY | O_NDELAY);
    if (fd == -1) {
        perror("Error opening serial port");
        return -1;
    }

    struct termios options;
    tcgetattr(fd, &options);
    cfsetispeed(&options, BAUD_RATE);
    cfsetospeed(&options, BAUD_RATE);
    options.c_cflag &= ~PARENB; // No parity
    options.c_cflag &= ~CSTOPB; // 1 stop bit
    options.c_cflag &= ~CSIZE;
    options.c_cflag |= CS8; // 8 data bits
    options.c_cflag |= CREAD | CLOCAL; // Enable receiver and set local mode
    tcsetattr(fd, TCSANOW, &options);

    return fd;
}

int main() {
    int serial_fd = init_serial(SERIAL_PORT);
    if (serial_fd == -1) {
        return 1;
    }

    char current_date[11];
    get_current_datetime(current_date, sizeof(current_date));
    current_date[10]='\0';
    // Open the file for appending
    char filename[50];
    snprintf(filename, sizeof(filename), "tracking_%s.txt", current_date);
    
    printf("Reading from serial port %s and writing to %s\n", SERIAL_PORT, filename);
    
    FILE *file = fopen(filename, "a");
    if (!file) {
        perror("Error opening file");
        close(serial_fd);
        return 1;
    }

    printf("Reading from serial port %s and writing to %s\n", SERIAL_PORT, filename);

    // Buffer to store incoming data
    char buffer[256];
    ssize_t bytes_read;

    while (1) {
        bytes_read = read(serial_fd, buffer, sizeof(buffer) - 1);
        if (bytes_read > 0) {
            buffer[bytes_read] = '\0'; // Null-terminate the buffer

            // Get current timestamp
            char timestamp[20];
            get_current_datetime(timestamp, sizeof(timestamp));

            // Print the timestamped data to the file
            fprintf(file, "[%s] %s", timestamp, buffer);
            fflush(file); // Ensure data is written to disk
        }
        usleep(10000); // Sleep for 100ms to avoid excessive CPU usage
    }

    close(file);
    close(serial_fd);
    return 0;
}
