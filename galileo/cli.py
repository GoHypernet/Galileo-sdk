#!/usr/bin/env python3
import sys
import argparse
import inspect
import traceback
import readline
readline.set_completer_delims(' \t\n')
import cmd
import os
from functools import partial
from glob import glob
from termcolor import colored, cprint
from getpass import getpass

import requests


from .api import API, RegistrationError


def matrix_to_table(matrix, sep='  '):
    if not matrix:
        return ''

    for row in matrix:
        if len(row) != len(matrix[0]):
            raise ValueError("matrix rows are of inonsistent lengths")

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

def print_ascii():
    print('   _____       _ _ _            ')
    print('  / ____|     | (_) |           ')
    print(' | |  __  __ _| |_| | ___  ___  ') 
    print(' | | |_ |/ _` | | | |/ _ \\/ _ \\ ') 
    print(' | |__| | (_| | | | |  __/ (_) |') 
    print('  \\_____|\\__,_|_|_|_|\\___|\\___/ ') 
    print('                                ') 
    print('                                ') 

class CLI(cmd.Cmd):
    intro = 'Welcome to Galileo!'
    prompt = 'Command (? for help): '
    file = None
    print_ascii()

    @staticmethod
    def init_parser():
        parser = argparse.ArgumentParser(description="Command line interface for Galileo")
        parser.add_argument('--username', default='', help="Username for login", type=str)
        parser.add_argument('--password', default='', help="Password for username", type=str)
        parser.add_argument('--cert', default=None, help="The SSL certificate for the daemon", type=str, required=False)
        parser.add_argument('--host', default='https://localhost', help="The IPv4 address of the controller",   type=str)
        parser.add_argument('--port', default=8080,        help="The port of the controller", type=int)
        return parser

    def __init__(self, username, password, host, port, cert):
        super().__init__()
        self.api = API(host, port, cert)
        self.api.login(username, password)
        self._upgrade_commands()

    def _param_completer(self, param, text, state):
        matches = self._matches(param, text)
        if state >= len(matches):
            return None
        return matches[state]

    def _arg_split_wrapper(self, func):
        params = list(inspect.signature(func).parameters.keys())
        def wrapper(arg=''):
            args = arg.split()
            old_completer = readline.get_completer()
            for param in params[len(args):]:
                readline.set_completer(partial(self._param_completer, param))
                args.append(input(f'  {param}: '))
            readline.set_completer(old_completer)

            try:
                return func(*args)
            except:
                print('Something went wrong with that command')
                print(traceback.format_exc())

        return wrapper

    def _matches(self, param, text):
        if param == 'group_id':
            return [x['id'] for x in self.api.groups() if x['id'].startswith(text)]
        if param == 'job_id':
            return []
        if param == 'landing_zone_id':
            return [x['id'] for x in self.api.landing_zones() if x['id'].startswith(text)]
        if param == 'launch_pad_id':
            return [x['id'] for x in self.api.launch_pads() if x['id'].startswith(text)]
        if param == 'machine_id':
            return [x['id'] for x in self.api.machines() if x['id'].startswith(text)]
        if param == 'path':
            paths = glob(text + '*')
            return [f'{x}{os.sep}' if os.path.isdir(x) else x for x in paths]
        return []

    def _make_arg_completer(self, func):
        params = list(inspect.signature(func).parameters.keys())
        def completer(text, line, beg_idx, end_idx):
            param_idx = len(line.split()) - 1
            if text:
                param_idx -= 1
            if param_idx >= len(params):
                return []
            param = params[param_idx]
            return self._matches(param, text)
        return completer

    def _make_helper(self, name, func):
        params = list(inspect.signature(func).parameters.keys())
        params = [f'<{x}>' for x in params]
        def helper():
            print(f'  {name}: {" ".join(params)}\n'
                  f'    {func.__doc__}')
        return helper

    def cmd_names(self):
        protected_cmds = {'do_help'}
        for name in self.get_names():
            if ((not name.startswith('do_')) or
                (name in protected_cmds)):
                continue
            yield name[3:]

    # Adds exit as a possible command that exits the cli
    def do_exit(self):
        return True

    def do_help(self, arg):
        '''
            Summary: Overrides the CMD class do_help option to display 
                     docstrings of commands and command groupings.

            Input:  Optional help argument being either a command or a 
                    grouping of commands like 'p2l', 'jobs', or 'groupings'.

            Output: Calls print_topics to generate colored output of 
                    commands and docstrings
        '''

        helps_of_groupings = [name for name in self.get_names() if name[:4] == 'help']
        if arg:
            # Check arg syntax
            try:
                func = getattr(CLI, 'help_' + arg)
            except AttributeError:
                try:
                    doc = getattr(CLI, 'do_' + arg).__doc__
                    if doc:
                        cmd = 'do_' + arg
                        self.print_topics(self.doc_header, [cmd], 12, 80)
                        return
                except AttributeError:
                    pass
                self.stdout.write("&s\n"%str(self.nohelp % (arg,)))
                return
            func(self)
        else:
            self.print_topics(self.doc_header, helps_of_groupings, 15, 80)

    def help_p2l(self):
        '''Stands for "permission to land."'''
        p2l_cmds = [cmd for cmd in self.get_names() if 'p2l' in cmd and cmd[:4] != 'help' and cmd != 'do_p2l']
        self.print_topics(self.doc_header, p2l_cmds, 15, 80)


    def help_groupings(self):
        '''Information on current groups you are in.'''
        groups_cmds = [cmd for cmd in self.get_names() if 'group' in cmd and cmd[:4] != 'help' and cmd != 'do_groupings']
        self.print_topics(self.doc_header, groups_cmds, 15, 80)


    def help_jobs(self):
        '''Running and seeing jobs.'''
        jobs_cmds = [cmd for cmd in self.get_names() if 'job' in cmd and cmd[:4] != 'help' and cmd != 'do_jobs']
        self.print_topics(self.doc_header, jobs_cmds, 15, 80)

    # Okay to override the print topics method in the cmd module?
    def print_topics(self, header, cmds, cmdlen, maxcol):
        if header:
            cprint(f'{str(header)}\n', 'cyan')
        if self.ruler:
            cprint(f'{str(self.ruler * len(header))}', 'cyan')
        if cmds:
            for cmd in cmds:
                first, second = cmd.split('_')
                spaces = 20 - len(second)
                doc_string = getattr(CLI, cmd).__doc__
                colored_cmd = colored(second, 'white', attrs=['bold'])
                print(f'{colored_cmd} {str(spaces * " ")}  {doc_string}')

        self.stdout.write('\n')  

    def do_jobs(self, *args):
        '''
            Summary: Arguments are parsed and functions are looked up in the cmd dictionary
                     in order to find the proper function name to call

            Input:   jobs command with optional command arguments

            Output:  The running of whatever do_ command the user input as an argument

        '''
        cmd_dict = self.generate_cmd_dictionary()
        if args[0] == 'download' and len(args) == 3:
            try:
                self.do_downloadjob(args[1], args[2])
            except:
                print(f'Arguments "{args[1]}" and "{args[2]}" are not valid.')
        elif args[0] in cmd_dict['job'].keys():
            try:
                func_name = cmd_dict['job'][args[0]]
                func_to_run = globals()[func_name]
                func_to_run(self, *args[1:])
            except:
                print('Your command failed to run with the listed arguments below:\n')
                for arg in args:
                    print(f'{arg} ')
        else:
            print(f'Argument {args[0]} is not a valid command within the groupings grouping.')

    def do_p2l(self, *args):
        '''
            Summary: Arguments are parsed and functions are looked up in the cmd dictionary
                     in order to find the proper function name to call

            Input:   p2l command with optional command arguments

            Output:  The running of whatever do_ command the user input as an argument

        '''
        cmd_dict = self.generate_cmd_dictionary()
        if args[0] in cmd_dict['p2l'].keys():
            try:
                func_name = cmd_dict['p2l'][args[0]]
                func_to_run = globals()[func_name]
                func_to_run(self, *args[1:])
            except:
                print('Your command failed to run with the listed arguments below:\n')
                for arg in args:
                    print(f'{arg} ')
        else:
            print(f'Argument {args[0]} is not a valid command within the p2l grouping.')


    def do_groupings(self,*args):
        '''
            Summary: Arguments are parsed and functions are looked up in the cmd dictionary
                     in order to find the proper function name to call

            Input:   groupings command with optional command arguments

            Output:  The running of whatever do_ command the user input as an argument

        '''
        cmd_dict = self.generate_cmd_dictionary()
        if args[0] == 'groups' and len(args) == 1:
            self.do_groups()
        elif args[0] in cmd_dict['group'].keys():
            try:
                func_name = cmd_dict['group'][args[0]]
                func_to_run = globals()[func_name]
                func_to_run(self, *args[1:])
            except:
                print('Your command failed to run with the listed arguments below:\n')
                for arg in args:
                    print(f'{arg} ')
        else:
            print(f'Argument {args[0]} is not a valid command within the groupings grouping.')

    def generate_cmd_dictionary(self):
        '''
            Summary: All functions are parsed and added to a dictionary depending on
                     what category they fall in. A reference to the function name
                     is stored along with the abbreviated versions that a user may
                     call on the command line. 

            Input:   None

            Output:  A dictionary with keys being groupings then values being another
                     dictionary containing abbreviated names and full function names.
 
        '''
        list_of_keywords = ['group', 'job', 'p2l']
        dictionary = dict.fromkeys(list_of_keywords, {})
        for func in self.get_names():
            if func[:3] == 'do_':
                name = func[3:]
                if 'groups' in name:
                    name = name.replace('groups', '')
                    dictionary['group'][name] = func
                elif 'jobs' in name:
                    name = name.replace('jobs', '')
                    dictionary['job'][name] = func
                elif 'group' in name:
                    name = name.replace('group', '')
                    dictionary['group'][name] = func
                elif 'job' in name:
                    name = name.replace('job', '')
                    dictionary['job'][name] = func
                elif 'p2l' in name:
                    name = name.replace('p2l', '')
                    dictionary['p2l'][name] = func
            else:
                pass
        return dictionary

    def _upgrade_commands(self):
        for name in self.cmd_names():
            func = getattr(self, f'do_{name}')
            setattr(self, f'complete_{name}', self._make_arg_completer(func))
            setattr(self, f'do_{name}', self._arg_split_wrapper(func))
            setattr(self, f'help_{name}', self._make_helper(name, func))

    def interpret(self):
        self.cmdloop()
        self.api.disconnect()

    def emptyline(self):
        return

    # Removed id and os from table
    def do_machines(self):
        'All machines on the network'
        machines = self.api.machines()
        print(dictlist_to_table(machines, ['name', 'owner_id', 'status']))

    # Removed id from table
    def do_localmachine(self):
        'Return information about this machine'
        print(dictlist_to_table([self.api.local_machine()], ['name', 'owner_id', 'status']))

    # Removed id from table
    def do_landingzones(self):
        'Machines you have P2L on'
        lzs = self.api.landing_zones()
        print(dictlist_to_table(lzs, ['name', 'owner_id', 'status']))

    def do_launchpads(self):
        'Users that have P2L on this machine'
        lps = self.api.launch_pads()
        print(list_to_table(lps))

    def do_sentp2lreqs(self):
        'Machines that have yet to respond to your request for P2L'
        reqs = self.api.p2l_requests_sent()
        print(dictlist_to_table(reqs, ['name', 'owner_id', 'status', 'id']))

    def do_recvdp2lreqs(self):
        'Users that have requested P2L on this machine and await your response'
        reqs = self.api.p2l_requests_recvd()
        print(list_to_table(reqs))

    def do_sentp2linvs(self):
        'Users that you have invited to land jobs on this machine'
        invs = self.api.p2l_invites_sent()
        print(list_to_table(invs))

    def do_recvdp2linvs(self):
        'Machines that have invited you to land jobs on them'
        invs = self.api.p2l_invites_recvd()
        print(dictlist_to_table(invs, ['name', 'owner_id', 'status', 'id']))

    # Removed admins, members, and machines from table
    def do_groups(self):
        'List of groups that you belong to'
        groups = self.api.groups()
        print(dictlist_to_table(groups, ['name', 'description', 'id', 'owner']))

    def do_sentgroupinvs(self, group_id):
        'Invitations to a group that you have sent'
        invs = self.api.group_invites_sent(group_id)
        print(list_to_table(invs))

    def do_recvdgroupinvs(self):
        'Groups to which you have received invitations'
        invs = self.api.group_invites_recvd()
        print(dictlist_to_table(invs, ['name', 'id', 'owner']))

    def do_sentgroupreqs(self):
        'Requests to join groups that you have sent'
        reqs = self.api.group_requests_sent()
        print(list_to_table(reqs))

    def do_recvdgroupreqs(self, group_id):
        'Pending requests from prospective members for groups that you administrate'
        reqs = self.api.group_requests_recvd(group_id)
        print(list_to_table(reqs))

    # Removed run_time and status_history from table
    def do_sentjobs(self):
        'Jobs that you have sent to a landing zone'
        jobs = self.api.sent_jobs()
        print(dictlist_to_table(jobs, ['name', 'landing_zone', 'id', 'status', 'results_path']))

    # Removed run_time and status_history from table
    def do_sentjob(self, job_id):
        'Jobs that you have sent to a landing zone'
        job = self.api.sentjob(job_id)
        print(dictlist_to_table([job], ['name', 'landing_zone', 'id', 'status']))

    # Removed run_time and status_history from table
    def do_recvdjobs(self):
        'Jobs that you have sent to a landing zone'
        jobs = self.api.received_jobs()
        print(dictlist_to_table(jobs, ['name', 'launch_pad', 'id', 'status']))

    # Removed run_time and status_history from table
    def do_recvdjob(self, job_id):
        'Jobs that you have sent to a landing zone'
        job = self.api.recvdjob(job_id)
        print(dictlist_to_table([job], ['name', 'landing_zone', 'id', 'status']))

    def do_sendp2lreq(self, landing_zone_id):
        'Request p2l on another machine'
        self.api.p2l_request(landing_zone_id)

    def do_withdrawp2lreq(self, landing_zone_id):
        'Stop requesting p2l on another machine'
        self.api.p2l_request_withdrawal(landing_zone_id)

    def do_acceptp2lreq(self, launch_pad_id):
        'Accept a p2l request'
        self.api.p2l_request_response(launch_pad_id, 'accept')

    def do_rejectp2lreq(self, launch_pad_id):
        'Reject a p2l request'
        self.api.p2l_request_response(launch_pad_id, 'reject')

    def do_sendp2linv(self, launch_pad_id):
        'Invite a user to land jobs on this machine'
        self.api.p2l_invite(launch_pad_id)

    def do_withdrawp2linv(self, launch_pad_id):
        'Stop inviting a user to land jobs on this machine'
        self.api.p2l_invite_withdrawal(launch_pad_id)

    def do_acceptp2linv(sel, landing_zone_id):
        'Accept a p2l invite'
        self.api.p2l_invite_response(landing_zone_id, 'accept')

    def do_rejectp2linv(sel, landing_zone_id):
        'Reject a p2l invite'
        self.api.p2l_invite_response(landing_zone_id, 'reject')

    def do_revokep2l(self, launch_pad_id):
        'Take away a user\'s p2l on this machine'
        self.api.p2l_revocation(launch_pad_id)

    def do_resignp2l(self, landing_zone_id):
        'Give up your p2l on some machine'
        self.api.p2l_resignation(landing_zone_id)

    def do_creategroup(self, name, description):
        'Create a new group'
        self.api.group_creation(name, description, [])

    def do_destroygroup(self, group_id):
        'Destroy a group that you own'
        self.api.group_destruction(group_id)

    def do_sendgroupinv(self, group_id, user_id):
        'Invite a user to join a group you administer'
        self.api.group_invite(group_id, user_id)

    def do_acceptgroupinv(self, group_id):
        'Accept an invitation to join a group'
        self.api.group_invite_response(group_id, 'accept')

    def do_rejectgroupinv(self, group_id):
        'Reject an invitation to join a group'
        self.api.group_invite_response(group_id, 'reject')

    def do_sendgroupreq(self, group_id):
        'Request to join a group'
        self.api.group_request(group_id)

    def do_acceptgroupreq(self, group_id, user_id):
        'Accept a request to join a group'
        self.api.group_request_response(group_id, user_id, 'accept')

    def do_rejectgroupreq(self, group_id, user_id):
        'Reject a request to join a group'
        self.api.group_request_response(group_id, user_id, 'reject')

    def do_leavegroup(self, group_id):
        'Elect to leave a group you belong to'
        self.api.group_withdrawal(group_id)

    def do_expelgroupmember(self, group_id, user_id):
        'Kick someone out of a group that you administrate'
        self.api.group_expulsion(group_id, user_id)

    def do_groupaddmachine(self, group_id, machine_id):
        'add machien'
        self.api.group_machine_addition(group_id, machine_id)

    def do_grouprmmachine(self, group_id, machine_id):
        'rm machien'
        self.api.group_machine_removal(group_id, machine_id)

    def do_submitjob(self, path, landing_zone_id):
        'submit a job to a landing zone'
        self.api.job_submit(path, landing_zone_id)

    def do_downloadjob(self, job_id, results_path):
        'Download the results of a completed job'
        self.api.job_download(job_id, results_path)

    def do_stopjob(self, job_id):
        'Stop a job'
        self.api.job_stop(job_id)

    def do_startjob(self, job_id):
        'Start a job'
        self.api.job_start(job_id)

    def do_pausejob(self, job_id):
        'Pause a job'
        self.api.job_pause(job_id)

    def do_topjob(self, job_id):
        'Top the process info of a job'
        self.api.job_top(job_id)

    def do_logjob(self, job_id):
        'Tail the stdout of a job'
        self.api.job_logs(job_id)

    def do_hidejob(self, job_id):
        'Hide a job'
        self.api.job_hide(job_id)

    def do_sharefolder(self, path):
        'Shares a folder'
        self.api.share_folder(path)

    def do_shutdown(self):
        'Shutdown'
        self.api.shutdown()

    def def_pid(self):
        'Get the server process id'
        self.api.pid()

    def do_sendlog(self, path):
        'Send your log to the backend'
        self.api.send_log(path)


def main(argv=sys.argv[1:]):
    args = CLI.init_parser().parse_args(argv)
    if ((args.username and not args.password) or
        (args.password and not args.username)):
        LOG.error("Username and password are required for login")
        sys.exit(1)

    while not (args.username and args.password):
        args.username = input("Username: ").strip()
        args.password = getpass("Password: ")

    cli = CLI(**vars(args))
    cli.interpret()


if __name__ == "__main__":
    main()
