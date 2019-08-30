# Event-based auto-accept script

## Overview
These two scripts allow the user to accept permission to land requests (`machine.py`), reject permission to land invitations, accept group invites, and add all of the user's machines to the group (`user.py`). There are two scripts in this example: one for users and one for machines. The user script only needs to be ran on one of the users' machines whereas the machine script must be ran on all machines that what to automatically accept incoming requests. This script takes advantage of event emitters and listeners.

## Running the script
1. To run these scripts, you must already have the Galileo daemon and Galileo CLI on two running terminals respectively. 
2. Open another terminal and run `python3 <path_to_script> --host <host_name> --port <port_number> --cert <cert_file>`, where `host_name` is the same as daemon and CLI host, `port_number` is same as daemon and CLI port, and `cert_file` is found where you ran the daemon. The prompt will ask you for your login information, which should be the same as the CLI login information.
3. Both scripts need to have their own terminal if you want to run them both at the same time.