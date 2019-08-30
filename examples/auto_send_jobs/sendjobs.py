#! /usr/bin/env python3
import sys
import argparse

from galileo.api import API as Galileo


def error(msg, exit_code=None):
    trace_indent = ' '*4
    print(msg)
    print(str(sys.exc_info()).replace('\n', f'{trace_indent}\n'))
    if exit_code != None:
        sys.exit(exit_code)


def main(host, port, cert, username, password, group, job):
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

    # Check if I have access to the group
    groups = []
    try:
        groups = galileo.groups()
    except:
        error(f"Could not get groups.")

    group_info = {}
    for g in groups:
        if group == g['name']:
            group_info = g

    if not group_info:
        error(f"You do not have group permissions.")

    # Get the IDs of all online machines within the group
    # print("This is groups info", group_info)
# print("\n\nThis is group info machine", group_info['machines'])
# print("\n\nThis is machines", galileo.machines())

    machines = []
    try:
        machines = galileo.machines()
    except:
        error(f"Could not get groups")

    targets = []
    for group_machine in group_info['machines']:
        for machine in machines:
            if (group_machine == machine['id']) and (machine['status'].upper() == 'ONLINE'):
                targets.append(group_machine)

    if not targets:
        print("No machines available to send job to.")

    # Send a job to each online machine within the group
    for machine_id in targets:
        try:
            galileo.job_submit(job, machine_id)
            print(f"Job sent to {machine_id}")
        except:
            error(f"Something went wrong with sending a job.")

def parse_args():
    parser = argparse.ArgumentParser(description="Commands a running Galileo daemon to automatically send jobs to a group. Requires that galileod is running.")
    parser.add_argument('--host', default='https://localhost', help="The IPv4 address of the daemon", type=str)
    parser.add_argument('--port', default=5000, help="The port of the daemon", type=int)
    parser.add_argument('--cert', default='galileod.crt', help="The SSL certificate for the daemon", type=str)
    parser.add_argument('--username', default='', help="Username for login", type=str)
    parser.add_argument('--password', default='', help="Password for username", type=str)
    parser.add_argument('--group', default='', help="The group you want to run jobs in", type=str)
    parser.add_argument('--job', default='', help="Directory of the job you want to run", type=str)

    args = sys.argv[1:]
    args = parser.parse_args(args)
    if ((args.username and not args.password) or
            (args.password and not args.username)):
        error("Username and password are required for login", 3)

    while not (args.username and args.password):
        args.username = input("Username: ").strip()
        args.password = input("Password: ").strip()

    while not (args.group and args.job):
        args.group = input("Group to send jobs to: ").strip()
        args.job = input("Job directory: ").strip()

    return vars(args)

if __name__ == "__main__":
    main(**parse_args())