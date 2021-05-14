#include <arpa/inet.h>
#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <time.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
	// Ingest environment variables
	char *lz_ipv4 = getenv("GALILEO_LZ_IPV4");
	char *lz_port = getenv("GALILEO_LZ_PORT");
	if (lz_ipv4 == NULL) {
		fprintf(stderr, "Missing GALILEO_LZ_IPV4 in environment\n");
		return 1;
	}
	if (lz_port == NULL) {
		fprintf(stderr, "Missing GALILEO_LZ_PORT in environment\n");
		return 1;
	}

	struct sockaddr_in lz_addr;
	lz_addr.sin_family = AF_INET;

	// Validate and convert IPv4 address
	int addr_conv_result = inet_pton(lz_addr.sin_family, lz_ipv4, &lz_addr.sin_addr);
	if (addr_conv_result == 0) {
		fprintf(stderr, "Invalid LZ IPV4: %s\n", lz_ipv4);
		return 1;
	} else if (addr_conv_result != 1) {
		perror("Error converting address string");
		return 1;
	}

	// Validate and convert port number
	char *invalid_port_char = '\0';
	long lz_port_num = strtol(lz_port, &invalid_port_char, 0);
	if ((*lz_port == '\0' || *invalid_port_char != '\0') || // check invalid chars
			(lz_port_num == LONG_MIN || lz_port_num == USHRT_MAX) || // check (under/over)flow
			(lz_port_num >= 2<<16 || lz_port_num < 0)) { // check boundaries of port range
		char *err_str;
		sprintf(err_str, "Invalid LZ Port: %s\n", lz_port);
		perror(err_str);
		return 1;
	}
	lz_addr.sin_port = htons((uint16_t) lz_port_num);

	// Open a socket
	int socket_fd = socket(lz_addr.sin_family, SOCK_STREAM, 0);
	if (socket_fd == -1) {
		perror("Error creating socket");
		return 1;
	}

	// Connect to the server
	if (connect(socket_fd,
							(struct sockaddr *)(&lz_addr),
							sizeof(lz_addr)) == -1) {
		perror("Error connecting to LZ");
		return 1;
	}

	// Send custom notifications!
	printf("Connected!\n");
	char message[100];
	time_t now;
	for (int i = 0; i < 6; ++i) {
		time(&now);
		sprintf(message, "Hello! %s", ctime(&now));
		printf("Sending message...\n");
		send(socket_fd, message, strlen(message), 0);
		printf("Done sending\n");
		sleep(10);
	}

	return 0;
}
