from urllib.parse import urlunparse, urljoin
from functools import partial
import json
import sys
import requests
from time import sleep
import socketio


class GalileoError(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return f'Code {self.code}: {self.msg}'


class LoginError(GalileoError):
    pass


class AuthorizationError(GalileoError):
    pass


class RegistrationError(GalileoError):
    pass


class API:
    """
    A Galileo API class.
    """

    def __init__(self, ctrl_addr, ctrl_port, ctrl_cert):
        """
        Initializes Galileo object.

        :param ctrl_addr: host address (e.g. 'https://localhost')
        :param ctrl_port: port of the host address (e.g. '5000')
        :param ctrl_cert: name of the certificate file (e.g. 'galileod.crt')
        """
        self.ctrl_addr = ctrl_addr
        self.ctrl_port = ctrl_port
        self.ctrl_cert = ctrl_cert

    def callback(self, code, msg=None):
        if code != 0:
            # TODO: raise an exception
            print(f'Encountered Error: Code {code}: {msg}')
        else:
            print(f'Success!')

    def get_tokens(self, username, password):
        """
        Get tokens for authentication.

        :param username: username
        :param password: password
        :return: None
        """
        data = {'username': username,
                'password': password,
                'client_version': 'To_Do'}
        url = urljoin(self.backend(), '/user/login')
        r = requests.post(url, json=data)
        r.raise_for_status()
        r = r.json()
        valid, code, msg = [r[x] for x in ['valid', 'code', 'msg']]
        if not valid or code != 0:
            raise LoginError(code, msg)

        self.access_token = r['token']
        self.refresh_token = r['refresh_token']

        # Authenticate
        self.headers = {'Authorization': f'Bearer {self.access_token}'}
        self._request = partial(self._request, headers=self.headers)

    def new_access_token(self):
        """
        Get new tokens for authentication.

        :return: response after POST request to refreshing tokens
        """
        url = urljoin(f'http://{self.backend()}', '/refresh/token')
        r = requests.post(url, json={'refresh_token': self.refresh_token})
        r.raise_for_status()
        return r.text

    def login(self, username, password):
        """
        Login.

        :param username: username
        :param password: password
        :return: None
        """
        # Get a token
        self.get_tokens(username, password)
        self.authenticate()
        self.register()
        self.create_socket_client()

    def create_socket_client(self):
        """
        Create new socket client, connect to the server, and emit a partial event.

        :return: None
        """
        self.sio = socketio.Client(logger=False)
        self.sio.connect(f'{self.ctrl_addr}:{self.ctrl_port}', headers=self.headers, certfile=self.ctrl_cert)
        self.sio.emit = partial(self.sio.emit, callback=self.callback)

    def _make_url(self, endpoint, params='', query='', fragment=''):
        """
        (Private) Make URL for HTTP request.

        :param endpoint: endpoint you want to hit
        :param params: parameters
        :param query: query component
        :param fragment: fragments
        :return: url
        """
        schema, addr = self.ctrl_addr.split('://')
        return urlunparse((schema, f'{addr}:{self.ctrl_port}', endpoint, params, query, fragment))

    def _request(self, request, endpoint, data=None, params='', query='', fragment='', headers=None):
        """
        (Private) Send an HTTP request.

        :param request: type of request such as 'requests.post' or 'requests.get'
        :param endpoint: endpoint you want to request to hit
        :param data: request body, data to send
        :param params: parameters
        :param query: query component
        :param fragment: fragments
        :param headers: headers for the request
        :return: request response
        """
        url = self._make_url(endpoint, params, query, fragment)
        r = request(url, json=data, verify=self.ctrl_cert, headers=headers)
        if r.status_code == 401:
            self.access_token = self.new_access_token()
            headers = {'Authorization': f'Bearer {self.access_token}'}
            r = request(url, json=data, verify=self.ctrl_cert, headers=headers)

        r.raise_for_status()
        return r

    def _get(self, *args, **kwargs):
        """
        (Private) Submit a HTTP GET request.

        :param args: endpoint you want to hit
        :param kwargs: request body, data to send
        :return: request response
        """
        return self._request(requests.get, *args, **kwargs)

    def _get_key(self, key, *args, **kwargs):
        """
        (Private)

        :param key:
        :param args: endpoint you want to hit
        :param kwargs: request body, data to send
        :return: request response
        """
        return self._get(*args, **kwargs).json()[key]

    def _post(self, *args, **kwargs):
        """
        (Private) Submit a HTTP POST request.

        :param args: endpoint you want to hit
        :param kwargs: request body, data to send
        :return: request response
        """
        return self._request(requests.post, *args, **kwargs)

    def _post_msg(self, *args, **kwargs):
        """
        (Private) Message of the HTTP POST request.

        :param args: endpoint you want to hit
        :param kwargs: request body, data to send
        :return: request response
        """
        return self._post(*args, **kwargs)['msg']

    def backend(self):
        """
        Gets name of the backend server currently being used.

        :return: name of the server
        """
        return self._get('backend').text

    def authenticate(self):
        """
        Authenticate tokens and introduce your user profile to the Galileo network.

        :return: response of POST request after authenticating tokens
        """
        return self._post('authenticate', {'refresh_token': self.refresh_token})

    def register(self):
        """
        Register machine to Galileo network to bring your machine online.
        :return: response of the POST request after registering
        """
        return self._post('register')

    def disconnect(self):
        """
        Disconnect from socket client.

        :return: None
        """
        self.sio.disconnect()

    def machines(self):
        """
        Get all machines on the network.

        :return: an object of all machines on the network.
        """
        return self._get('machines').json()

    def local_machine(self):
        """
        Get information about your machine.

        :return: an object with information about your machine
        """
        return self._get('local_machine').json()

    def landing_zones(self):
        """
        Machines that you can land a job on.

        :return: an object of machines you can land on
        """
        return self._get('landing_zones').json()

    def launch_pads(self):
        """
        Users that have permission to land on the current machine.

        :return: an object of users that can land on your machine
        """
        return self._get('launch_pads').json()

    def p2l_requests_sent(self):
        """
        Get all permission to land requests you have sent.

        :return: an object of all requests you have sent
        """
        return self._get('p2l_requests_sent').json()

    def p2l_requests_recvd(self):
        """
        Get all permission to land requests you have received.

        :return: an object of all requests you have received.
        """
        return self._get('p2l_requests_recvd').json()

    def p2l_invites_sent(self):
        """
        Get all permission to land invitations you have sent.

        :return: an object of all invitations you have sent
        """
        return self._get('p2l_invites_sent').json()

    def p2l_invites_recvd(self):
        """
        Get all permission to land invitations you have received.

        :return: an object of all invitations you have sent
        """
        return self._get('p2l_invites_recvd').json()

    def sentjob(self, job_id):
        """
        Get a job the user had sent.

        :param job_id: the job ID string
        :return: an object describing related information of job
        """
        return self._get(f'sent_jobs/{job_id}').json()

    def recvdjob(self, job_id):
        """
        Get a job the user had received.

        :param job_id: the job ID string
        :return: an object describing related information of job
        """
        return self._get(f'recvd_jobs/{job_id}').json()

    def groups(self):
        """
        Get all groups the user belongs in and related information about the groups.

        :return: an object describing all the groups that the user is in
        """
        return self._get('groups').json()

    def group_invites_sent(self, group_id):
        """
        Get all group invitations the user has sent out for a single group.

        :param group_id: the group ID string
        :return: an object describing all the group invitations
        """
        return self._get(f'group_invites_sent/{group_id}').json()

    def group_invites_recvd(self):
        """
        Get all group invitations the user has received.

        :return: an object describing all group invitations the user has received
        """
        return self._get('group_invites_recvd').json()

    def group_requests_sent(self):
        """
        Get all groups requests the user has sent.

        :return: an object describing all group requests the user has sent
        """
        return self._get('group_requests_sent').json()

    def group_requests_recvd(self, group_id):
        """
        Get all groups requests the user has received.

        :return: an object describing all group requests the user has received
        """
        return self._get(f'group_requests_recvd/{group_id}').json()

    def sent_jobs(self):
        """
        Get all the jobs that you have sent.

        :return: an object describing all the jobs you have sent
        """
        return self._get(f'sent_jobs').json()

    def received_jobs(self):
        """
        Get all the jobs you have received.

        :return: an object describing all the jobs you have received
        """
        return self._get(f'recvd_jobs').json()

    def p2l_request(self, landing_zone_id):
        """
        Send a permission to land request to a machine.

        :param landing_zone_id: machine's ID string
        :return: None
        """
        self.sio.emit('p2l_request', landing_zone_id)

    def p2l_request_withdrawal(self, landing_zone_id):
        """
        Withdraw a permission to land request to a machine that the user had already sent.

        :param landing_zone_id: machine's ID string
        :return: None
        """
        self.sio.emit('p2l_request_withdrawal', landing_zone_id)

    def p2l_request_response(self, launch_pad_id, response):
        """
        The response to a permission to land request.

        :param launch_pad_id: username
        :param response: a string that can be either "accept" or "reject"
        :return: None
        """
        self.sio.emit('p2l_request_response', (launch_pad_id, response))

    def p2l_invite(self, launch_pad_id):
        """
        Send an invite to another user to land on the machine you sent the invite from.

        :param launch_pad_id: username
        :return: None
        """
        self.sio.emit('p2l_invite', launch_pad_id)

    def p2l_invite_withdrawal(self, launch_pad_id):
        """
        Revoke an invitation to land from a user.

        :param launch_pad_id: username
        :return: None
        """
        self.sio.emit('p2l_invite_withdrawal', launch_pad_id)

    def p2l_invite_response(self, landing_zone_id, response):
        """
        Respond to an invite to land on someone else's machine.

        :param landing_zone_id: machine's ID string
        :param response: a string that can be either "accept" or "reject"
        :return: None
        """
        self.sio.emit('p2l_invite_response', (landing_zone_id, response))

    def p2l_revocation(self, launch_pad_id):
        """
        Revoke a user's right to land on your machine.

        :param launch_pad_id: username
        :return: None
        """
        self.sio.emit('p2l_revocation', launch_pad_id)

    def p2l_resignation(self, landing_zone_id):
        """
        Resign from landing on a person's machine.

        :param landing_zone_id: machine's ID string
        :return: None
        """
        self.sio.emit('p2l_resignation', landing_zone_id)

    def group_creation(self, name, desc, invitees):
        """
        Create a new group.

        :param name: name of group
        :param desc: description of group
        :param invitees: users that are invited into the group
        :return: None
        """
        self.sio.emit('group_creation', (name, desc, invitees))

    def group_destruction(self, group_id):
        """
        Destroy your existing group.

        :param group_id: the ID of group that you want to destroy
        :return: None
        """
        self.sio.emit('group_destruction', group_id)

    def group_invite(self, group_id, user_id):
        """
        Invite a user to a group that you administer.

        :param group_id: group ID string
        :param user_id: user that you want to add to the group
        :return: None
        """
        self.sio.emit('group_invite', (group_id, user_id))

    def group_invite_response(self, group_id, response):
        """
        Response to an invitation to a group.

        :param group_id: group ID string
        :param response: a string that can either be "accept" or "reject"
        :return: None
        """
        self.sio.emit('group_invite_response', (group_id, response))

    def group_request(self, group_id):
        """
        Send a request for permission to land to all machines in a group you are a part of.

        :param group_id: ID of the group
        :return: None
        """
        self.sio.emit('group_request', group_id)

    def group_request_response(self, group_id, username, response):
        """
        Respond to a permission to land request from a group.

        :param group_id: group ID string
        :param username: username of the user who requested to land
        :param response: a string that can either be "accept" or "reject"
        :return: None
        """
        self.sio.emit('group_request_response', (group_id, username, response))

    def group_withdrawal(self, group_id):
        """
        Leave a group you are a part of.

        :param group_id: ID of the group you want to leave
        :return: None
        """
        self.sio.emit('group_withdrawal', group_id)

    def group_expulsion(self, group_id, username):
        """
        Remove a user from a group you administer.

        :param group_id: group ID string
        :param username: user you want to remove
        :return: None
        """
        self.sio.emit('group_expulsion', (group_id, username))

    def group_machine_addition(self, group_id, machine_id):
        """
        Add a machine to a group.

        :param group_id: group ID string
        :param machine_id: ID string of the machine you want to add to the group
        :return: None
        """
        self.sio.emit('group_machine_addition', (group_id, machine_id))

    def group_machine_removal(self, group_id, machine_id):
        """
        Remove a machine from a group.

        :param group_id: group ID string
        :param machine_id: ID string of the machine you want to remove from the group
        :return: None
        """
        self.sio.emit('group_machine_removal', (group_id, machine_id))

    def job_submit(self, path, landing_zone_id):
        """
        Submit a job to a machine.

        :param path: path of the job you want to send
        :param landing_zone_id: machine ID string you want the job to run on
        :return: None
        """
        self.sio.emit('job_submit', (path, landing_zone_id))

    def job_download(self, job_id, results_path):
        """
        Download the results of a launched job that has completed

        :param job_id: Job ID string
        :param results_path: A file system path to store the results in
        :return: None
        """
        self.sio.emit('job_download', (job_id, results_path))

    def job_stop(self, job_id):
        """
        Stop a running job.

        :param job_id: job ID string
        :return: None
        """
        self.sio.emit('job_stop', job_id)

    def job_start(self, job_id):
        """
        Start a job.

        :param job_id: job ID string
        :return: None
        """
        self.sio.emit('job_start', job_id)

    def job_pause(self, job_id):
        """
        Pause a running job.

        :param job_id: job ID string
        :return: None
        """
        self.sio.emit('job_pause', job_id)

    def job_top(self, job_id):
        """
        Get process status à la 'docker top'

        :param job_id: job ID string
        :return: None
        """
        self.sio.emit('job_top', job_id)

    def job_logs(self, job_id):
        """
        Get the current stdout of a job

        :param job_id: job ID string
        :return: None
        """
        self.sio.emit('job_logs', job_id)

    def job_hide(self, job_id):
        """
        Hide the current received and sent job list.

        :param job_id: job ID string
        :return: None
        """
        self.sio.emit('job_hide', job_id)

    def share_folder(self, path):
        """
        Initializes a path to a folder so that the files in the folder do not get copied over to the landing zone.

        :param path: path to a non-local source
        :return: None
        """
        self.sio.emit('share_folder', path)

    def shutdown(self):
        """
        Close the Galileo daemon.

        :return: None
        """
        self.sio.emit('shutdown')

    def send_log(self, path=None):
        """
        Send logs to the specified path.

        :param path: path where logs will be kept
        :return:
        """
        self.sio.emit('send_log', path)

    def pid(self):
        """
        Get process ID of Galileo daemon.

        :return: process ID
        """
        return self._get('pid').text
