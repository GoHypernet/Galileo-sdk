#! /usr/bin/env python3
from time import sleep
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
    # First, connect to Galileo by creating an instance.
    try:
        galileo = Galileo(host, port, cert)
    except:
        error(f"Could not connect to Galileo at {host} on port {port} with cert {cert}.", 1)

    # Get the tokens for authentication.
    try:
        galileo.get_tokens(username, password)
        galileo.create_socket_client()
    except:
        error("Could not get token with given username and password.", 2)

    while True:
        # Decline all invites from members that want you to land on their machine.
        invites = []
        try:
            invites = galileo.p2l_invites_recvd()
        except:
            error("Something went wrong with getting permission to land invites.")

        for member in invites:
            owner = member['owner_id']
            uuid = member['id']
            try:
                print(f"Declining invite from: '{owner}' -- '{uuid}'.")
                galileo.p2l_invite_response(uuid, "reject")
            except:
                error(f"Something went wrong while declining invite to '{owner}' -- '{uuid}'.")

        # Accept all groups that have invited you.
        group_invites = []
        try:
            group_invites = galileo.group_invites_recvd()
        except:
            error("Cannot get group invites received.")

        group_invites_id = [group['id'] for group in group_invites]
        for gid in group_invites_id:
            try:
                print(f"Accepting group invite from: {gid}.")
                galileo.group_invite_response(gid, "accept")
            except:
                error(f"Something went wrong while accepting invite to '{gid}'.")

        # Poll until you're added into all groups i.e. your received group invites are a subset within your groups.
        current_groups = []
        current_groups_ids = []
        while group_invites:
            try:
                current_groups = galileo.groups()
            except:
                error(f"Something went wrong while retrieving groups.")

            if current_groups:
                current_groups_ids = [groups['id'] for groups in current_groups]
                if set(group_invites_id).issubset(set(current_groups_ids)):
                    break
            sleep(2)

        # Get all your machines.
        owner_id = galileo.local_machine()['owner_id']
        machines = []
        try:
            machines = [machine['id'] for machine in galileo.machines() if machine['owner_id'] == owner_id]
        except:
            error(f"Something went wrong while getting machines.")

        # Add your machines to all your groups.
        groups_existing_machines = {groups['id']: groups['machines'] for groups in current_groups}

        if current_groups_ids:
            for gid in current_groups_ids:
                for machine_id in machines:
                    if machine_id not in groups_existing_machines[gid]:
                        try:
                            print(f"Adding machine '{machine_id}' to group '{gid}'.")
                            galileo.group_machine_addition(gid, machine_id)
                        except:
                            error(f"Something went wrong while adding machine '{machine_id}' to group '{gid}'.")

        sleep(2)


def parse_args():
    parser = argparse.ArgumentParser(description="Commands a running Galileo daemon to automatically accept all P2L requests and group invitations. Requires that galileod and galileo-cli are running.")
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