# Sending jobs script

## Overview
This script allows the user to send a job to all online machines in a group. 

## Running the script
1. To run these scripts, you must already have the Galileo daemon and Galileo CLI on two running terminals respectively. 
2. Open another terminal and run `python3 <path_to_script> --host <host_name> --port <port_number> --cert <cert_file> --group <group_name> --job <job_path>`, where `host_name` is the same as daemon and CLI host, `port_number` is same as daemon and CLI port, and `cert_file` is found where you ran the daemon. The prompt will ask you for your login information, which should be the same as the CLI login information. The prompt will also ask for the group name and the job path if not provided.