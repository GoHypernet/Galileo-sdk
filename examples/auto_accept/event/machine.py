#! /usr/bin/env python3
"""This script allows you to automatically accept all users that are requesting to land on your machine."""

import sys
import argparse
from galileo.api import API as Galileo


def error(msg, exit_code=None):
    trace_indent = ' '*4
    print(msg)
    print(str(sys.exc_info()).replace('\n', f'{trace_indent}\n'))
    if exit_code != None:
        sys.exit(exit_code)


def main(host, port, cert, username, password):
    # First, connect to Galileo by creating an instance
    try:
        galileo = Galileo(host, port, cert)
    except:
        error(f"Could not connect to Galileo at {host} on port {port} with cert {cert}.", 1)

    # Get the tokens for authentication
    try:
        galileo.get_tokens(username, password)  # Get the tokens for authentication
        galileo.create_socket_client()  # Create a socket.io client and connect to the server
    except:
        error("Could not get token with given username and password.", 2)

    # Listener will listen for p2l requests and accept.
    @galileo.sio.on('p2l_request')
    def on_p2l_request(launch_pad_id):
        try:
            print(f"Accept request from: {launch_pad_id}")
            galileo.p2l_request_response(launch_pad_zone_id, "accept")
        except:
            error(f"Something went wrong while accepting request from '{launch_pad_id}'.")

def parse_args():
    parser = argparse.ArgumentParser(description="Commands a running Galileo daemon to automatically accept all P2L "
                                                 "requests. Requires that galileod and galileo-cli are running.")
    parser.add_argument('--host', default='https://localhost', help="The IPv4 address of the daemon", type=str)
    parser.add_argument('--port', default=5000, help="The port of the daemon", type=int)
    parser.add_argument('--cert', default='galileod.crt', help="The SSL certificate for the daemon", type=str)
    parser.add_argument('--username', default='', help="Username for login", type=str)
    parser.add_argument('--password', default='', help="Password for username", type=str)

    args = sys.argv[1:]
    args = parser.parse_args(args)
    if ((args.username and not args.password) or
            (args.password and not args.username)):
        error("Username and password are required for login", 3)

    while not (args.username and args.password):
        args.username = input("Username: ").strip()
        args.password = input("Password: ").strip()

    return vars(args)


if __name__ == "__main__":
    main(**parse_args())
