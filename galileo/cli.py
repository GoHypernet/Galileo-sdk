#!/usr/bin/env python3
import sys
import argparse
import json
import inspect
import traceback
from datetime import datetime
from collections import OrderedDict


import requests


from .api import API, RegistrationError


def matrix_to_table(matrix, sep='  '):
    if not matrix:
        return ''

    for row in matrix:
        if len(row) != len(matrix[0]):
            raise ValueError("matrix rows are of inconsistent lengths")

    max_widths = [0] * len(matrix[0])
    for row in matrix:
        for col, val in enumerate(row):
            if len(str(val)) > max_widths[col]:
                max_widths[col] = len(str(val))

    fmt_strs = [f'{{:<{w}}}' for w in max_widths]

    s = '\n'.join([
        sep.join([fmt_str.format(val) for fmt_str, val in zip(fmt_strs, row)])
        for row in matrix])
    return s


def dictlist_to_table(dictlist, keys, headers=None):
    matrix = [headers] if headers else [keys]
    for _dict in dictlist:
        matrix.append([str(_dict[key]) for key in keys])
    return matrix_to_table(matrix)

def list_to_table(l):
    matrix = [[x] for x in l]
    return matrix_to_table(matrix)

class Command:
    def __init__(self, names, doc, action, prompts=[]):
        if isinstance(names, str):
            names = [names]
        if len(names) != len(set(names)):
            raise ValueError(f"Cannot create command with redundant names: {names}")
        self.names = names
        self.doc = doc
        self.action = action
        self.prompts = prompts

    def run(self, indent):
        kwargs = {}
        for var, metavar in self.prompts:
            kwargs[var] = input(f'{indent}{metavar}: ').strip()
        return self.action(**kwargs)

    def help_msg(self, indent):
        return f"{indent}{', '.join(self.names):15}\t\t\t{self.doc}"

class Commander:
    def __init__(self, indent_len=4):
        self.indent = ' ' * indent_len
        self.prompt = "Command (h for help): "
        self.name_to_cmd = OrderedDict()
        self.add_cmd(['help', 'h'], doc="Print this information", action=self.help)
        self.add_cmd(['quit', 'q', 'exit'], doc="Quit the interpreter", action=self.quit)

    def print(self, *objects, **kwargs):
        objects = [str(obj).replace('\n', f'{self.indent}\n') for obj in objects]
        if 'end' in kwargs:
            kwargs['end'] = kwargs['end'].replace('\n', f'{self.indent}\n')
        else:
            kwargs['end'] = f'{self.indent}\n'
        print(*objects, **kwargs)

    @property
    def cmds(self):
        return OrderedDict.fromkeys(self.name_to_cmd.values()).keys()

    def help(self):
        help_msgs = [cmd.help_msg(self.indent) for cmd in self.cmds]
        return '\n'.join(help_msgs)

    def quit(self):
        self.do_loop = False

    def cmd(self, names, doc, prompts=[]):
        def wrap(func, prompts=prompts):
            params = inspect.signature(func).parameters.keys()
            if prompts:
                if len(params) != len(prompts):
                    raise ValueError("Inequal number of prompts and parameters")
            else:
                prompts = [p.replace('_',' ').title() for p in params]
            prompts = list(zip(params, prompts))
            self.add_cmd(names, doc=doc, action=func, prompts=prompts)
            return func
        return wrap

    def add_cmd(self, names, doc, action, prompts=[]):
        cmd = Command(names, doc=doc, action=action, prompts=prompts)
        for name in cmd.names:
            if name in self.name_to_cmd:
                raise ValueError(f"Duplicated command name: {name}")
            self.name_to_cmd[name] = cmd

    def loop(self):
        self.do_loop = True
        while self.do_loop:
            name = input(self.prompt).strip()
            if name not in self.name_to_cmd:
                print(f"{self.indent}Unrecognized command name: {name}")
                continue

            try:
                print(self.name_to_cmd[name].run(self.indent))
            except Exception as e:
                self.print("Something went wrong with that call")
                self.print(traceback.format_exc())
                continue


class CLI:
    def __init__(self, username, password, host, port, cert):
        self.api = API(host, port, cert)
        self.api.login(username, password)
        self.init_cmdr()

    # TODO: make formatter print default values
    @staticmethod
    def init_parser():
        parser = argparse.ArgumentParser(description="Command line interface for Galileo")
        parser.add_argument('--username', default='', help="Username for login", type=str)
        parser.add_argument('--password', default='', help="Password for username", type=str)
        parser.add_argument('--cert', default=None, help="The SSL certificate for the daemon", type=str, required=False)
        parser.add_argument('--host', default='https://localhost', help="The IPv4 address of the controller",   type=str)
        parser.add_argument('--port', default=8080,        help="The port of the controller", type=int)
        return parser

    def interpret(self):
        self.cmdr.loop()
        self.api.disconnect()

    # TODO: get good doc msgs directly from __doc__ properties of app endpoints
    def init_cmdr(self):
        self.cmdr = Commander()

        @self.cmdr.cmd('machines', 'All machines on the network')
        def machines():
            machines = self.api.machines()
            return dictlist_to_table(machines, ['name', 'owner_id', 'status', 'id', 'os'])

        @self.cmdr.cmd('localmachine', 'Return information about this machine')
        def local_machine():
            return dictlist_to_table([self.api.local_machine()], ['name', 'owner_id', 'status', 'id'])

        @self.cmdr.cmd('landingzones', 'Machines you have P2L on')
        def landing_zones():
            lzs = self.api.landing_zones()
            return dictlist_to_table(lzs, ['name', 'owner_id', 'status', 'id'])

        @self.cmdr.cmd('launchpads', 'Users that have P2L on this machine')
        def launch_pads():
            lps = self.api.launch_pads()
            return list_to_table(lps)

        @self.cmdr.cmd('sentp2lreqs', 'Machines that have yet to respond to your request for P2L')
        def sent_p2l_requests():
            reqs = self.api.p2l_requests_sent()
            return dictlist_to_table(reqs, ['name', 'owner_id', 'status', 'id'])

        @self.cmdr.cmd('recvdp2lreqs', 'Users that have requested P2L on this machine and await your response')
        def recvd_p2l_requests():
            reqs = self.api.p2l_requests_recvd()
            return list_to_table(reqs)

        @self.cmdr.cmd('sentp2linvs', 'Users that you have invited to land jobs on this machine')
        def sent_p2l_invs():
            invs = self.api.p2l_invites_sent()
            return list_to_table(invs)

        @self.cmdr.cmd('recvdp2linvs', 'Machines that have invited you to land jobs on them')
        def recvd_p2l_invs():
            invs = self.api.p2l_invites_recvd()
            return dictlist_to_table(invs, ['name', 'owner_id', 'status', 'id'])

        @self.cmdr.cmd('groups', 'List of groups that you belong to')
        def groups():
            groups = self.api.groups()
            return dictlist_to_table(groups, ['name', 'description', 'id', 'owner', 'admins', 'members', 'machines'])

        @self.cmdr.cmd('sentgroupinvs', 'Invitations to a group that you have sent', ['group_id'])
        def sent_group_invs(group_id):
            invs = self.api.group_invites_sent(group_id)
            return list_to_table(invs)

        @self.cmdr.cmd('recvdgroupinvs', 'Groups to which you have received invitations')
        def recvd_group_invs():
            invs = self.api.group_invites_recvd()
            return dictlist_to_table(invs, ['name', 'id', 'owner'])

        @self.cmdr.cmd('sentgroupreqs', 'Requests to join groups that you have sent')
        def sent_group_reqs():
            reqs = self.api.group_requests_sent()
            return list_to_table(reqs)

        @self.cmdr.cmd('recvdgroupreqs', 'Pending requests from prospective members for groups that you administrate', ['group_id'])
        def recvd_group_reqs(group_id):
            reqs = self.api.group_requests_recvd(group_id)
            return list_to_table(reqs)

        @self.cmdr.cmd('sentjobs', 'Jobs that you have sent to a landing zone')
        def sent_jobs():
            jobs = self.api.sent_jobs()
            return dictlist_to_table(jobs, ['name', 'landing_zone', 'id', 'status', 'run_time', 'results_path', 'status_history'])

        @self.cmdr.cmd('sentjob', 'Jobs that you have sent to a landing zone', ['job_id'])
        def sent_job(job_id):
            job = self.api.sentjob(job_id)
            return dictlist_to_table([job], ['name', 'landing_zone', 'id', 'status', 'run_time', 'status_history'])

        @self.cmdr.cmd('recvdjobs', 'Jobs that you have sent to a landing zone')
        def recvd_jobs():
            jobs = self.api.received_jobs()
            return dictlist_to_table(jobs, ['name', 'launch_pad', 'id', 'status', 'run_time', 'status_history'])

        @self.cmdr.cmd('recvdjob', 'Jobs that you have sent to a landing zone', ['job_id'])
        def recvd_job(job_id):
            job = self.api.recvdjob(job_id)
            return dictlist_to_table([job], ['name', 'landing_zone', 'id', 'status', 'run_time', 'status_history'])

        self.cmdr.cmd('sendp2lreq',   'Request p2l on another machine', ['landing_zone_id'])(self.api.p2l_request)
        self.cmdr.cmd('withdrawp2lreq', 'Stop requesting p2l on another machine', ['landing_zone_id'])(self.api.p2l_request_withdrawal)
        self.cmdr.cmd('acceptp2lreq', 'Accept a p2l request', ['launch_pad_id'])(lambda x: self.api.p2l_request_response(x, 'accept'))
        self.cmdr.cmd('rejectp2lreq', 'Reject a p2l request', ['launch_pad_id'])(lambda x: self.api.p2l_request_response(x, 'reject'))
        self.cmdr.cmd('sendp2linv',   'Invite a user to land jobs on this machine', ['launch_pad_id'])(self.api.p2l_invite)
        self.cmdr.cmd('withdrawp2linv', 'Stop inviting a user to land jobs on this machine', ['launch_pad_id'])(self.api.p2l_invite_withdrawal)
        self.cmdr.cmd('acceptp2linv', 'Accept a p2l invite', ['landing_zone_id'])(lambda x: self.api.p2l_invite_response(x, 'accept'))
        self.cmdr.cmd('rejectp2linv', 'Reject a p2l invite', ['landing_zone_id'])(lambda x: self.api.p2l_invite_response(x, 'reject'))
        self.cmdr.cmd('revokep2l', 'Take away a user\'s p2l on this machine', ['launch_pad_id'])(self.api.p2l_revocation)
        self.cmdr.cmd('resignp2l', 'Give up your p2l on some machine', ['landing_zone_id'])(self.api.p2l_resignation)
        self.cmdr.cmd('creategroup', 'Create a new group', ['Name', 'Description'])(lambda x, y: self.api.group_creation(x, y, []))
        self.cmdr.cmd('destroygroup', 'Destroy a group that you own', ['group_id'])(self.api.group_destruction)
        self.cmdr.cmd('sendgroupinv', 'Invite a user to join a group you administer', ['group_id', 'username'])(self.api.group_invite)
        self.cmdr.cmd('acceptgroupinv', 'Accept an invitation to join a group', ['group_id'])(lambda x: self.api.group_invite_response(x, 'accept'))
        self.cmdr.cmd('rejectgroupinv', 'Reject an invitation to join a group', ['group_id'])(lambda x: self.api.group_invite_response(x, 'reject'))
        self.cmdr.cmd('sendgroupreq', 'Request to join a group', ['group_id'])(self.api.group_request)
        self.cmdr.cmd('acceptgroupreq', 'Accept a request to join a group', ['group_id', 'username'])(lambda x, y: self.api.group_request_response(x, y, 'accept'))
        self.cmdr.cmd('rejectgroupreq', 'Reject a request to join a group', ['group_id', 'username'])(lambda x, y: self.api.group_request_response(x, y, 'reject'))
        self.cmdr.cmd('leavegroup', 'Elect to leave a group you belong to', ['group_id'])(self.api.group_withdrawal)
        self.cmdr.cmd('expelgroupmember', 'Kick someone out of a group that you administrate', ['group_id', 'username'])(self.api.group_expulsion)
        self.cmdr.cmd('groupaddmachine', 'add machien', ['group_id', 'machine_id'])(self.api.group_machine_addition)
        self.cmdr.cmd('grouprmmachine', 'rm machien', ['group_id', 'machine_id'])(self.api.group_machine_removal)
        self.cmdr.cmd('submitjob', 'submit a job to a landing zone', ['path', 'landing_zone_id'])(self.api.job_submit)
        self.cmdr.cmd('stopjob', 'Stop a job', ['job_id'])(self.api.job_stop)
        self.cmdr.cmd('startjob', 'Start a job', ['job_id'])(self.api.job_start)
        self.cmdr.cmd('pausejob', 'Pause a job', ['job_id'])(self.api.job_pause)
        self.cmdr.cmd('hidejob', 'Hide a job', ['job_id'])(self.api.job_hide)
        self.cmdr.cmd('sharefolder', 'Shares a folder', ['path'])(self.api.share_folder)
        self.cmdr.cmd('shutdown', 'Shutdown')(self.api.shutdown)
        self.cmdr.cmd('pid', 'Get the server process id')(self.api.pid)
        self.cmdr.cmd('sendlog', 'Send your log to the backend', ['path'])(self.api.send_log)

def main(argv=sys.argv[1:]):
    args = CLI.init_parser().parse_args(argv)
    if ((args.username and not args.password) or
        (args.password and not args.username)):
        LOG.error("Username and password are required for login")
        sys.exit(1)

    while not (args.username and args.password):
        args.username = input("Username: ").strip()
        args.password = input("Password: ").strip()

    cli = CLI(**vars(args))
    cli.interpret()


if __name__ == "__main__":
    main()
