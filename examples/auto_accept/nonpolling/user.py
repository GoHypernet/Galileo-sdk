#! /usr/bin/env python3
"""This script allows you to automatically accept all groups invitations and add your machines to the group."""

import sys
import argparse
from galileo.api import API as Galileo


def error(msg, exit_code=None):
    trace_indent = ' ' * 4
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

    try:
        galileo.get_tokens(username, password)  # Get the tokens for authentication
        galileo.create_socket_client()  # Create a socket.io client and connect to the server
    except:
        error("Could not get token with given username and password.", 2)

    # Listener will listen for p2l invites and decline
    @galileo.sio.on('p2l_invite')
    def on_p2l_invite(landing_zone_id):
        # Decline all invites from members that want you to land on their machine
        try:
            print(f"Declining invite from: '{landing_zone_id}'.")
            galileo.p2l_invite_response(landing_zone_id, "reject")
        except:
            error(f"Something went wrong while declining invite to '{landing_zone_id}'.")

    # Listener will listen for group invites and accept.
    @galileo.sio.on('group_invite')
    def on_group_invites(group_id):
        try:
            print(f"Accepting group invite from: {group_id}.")
            galileo.group_invite_response(group_id, "accept")
        except:
            error(f"Something went wrong while accepting invite to '{group_id}'.")

    # After accepting the group, add all of your machines to the group
    @galileo.sio.on('group_invite_response_user')
    def on_group_invite_response_user(group_id, response):
        if response == "accept":
            owner_id = galileo.local_machine()['owner_id']

            machines = []
            try:
                machines = [machine['id'] for machine in galileo.machines() if machine['owner_id'] == owner_id]
            except:
                error("Something went wrong while getting machines.")

            for machine_id in machines:
                try:
                    print(f"Adding machine '{machine_id}' to group '{group_id}'.")
                    galileo.group_machine_addition(group_id, machine_id)
                except:
                    error(f"Something went wrong while adding machine '{machine_id}' to group '{group_id}'.")


def parse_args():
    parser = argparse.ArgumentParser(description="Commands a running Galileo daemon to automatically accept all group "
                                                 "invitations and add your machines to the group. Requires that "
                                                 "galileod and galileo-cli are running.")
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
