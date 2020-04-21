#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import argparse
from tpssh.teampass import TeampassClient
from tpssh.teampass.exceptions import TeampassApiException


def set_proc_name(newname):
    from ctypes import cdll, byref, create_string_buffer
    libc = cdll.LoadLibrary('libc.so.6')
    buff = create_string_buffer(len(newname) + 1)
    buff.value = newname
    libc.prctl(15, byref(buff), 0, 0, 0)


def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""
    from shutil import which
    return which(name) is not None


def spw(teampass_endpoint, teampass_token, host, username, parameters=None):
    tp = TeampassClient(teampass_endpoint, teampass_token)
    try:
        result = tp.search("item", host)
    except TeampassApiException:
        result = []
    if len(result) == 0:
        if len(username) != 0:
            cmd = 'ssh %s@%s %s' % (username, host, ' '.join(str(param) for param in parameters) if parameters else '')
        else:
            print("Username not set")
            sys.exit(1)
    elif len(result) == 1:
        if is_tool('sshpass'):
            cmd = 'sshpass -p %s ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no -o StrictHostKeyChecking=no %s@%s %s' % (result[0]['Password'], result[0]['Login'], host, ' '.join(str(param) for param in parameters) if parameters else '')
        else:
            print('sshpass util must be installed')
            sys.exit(1)
    else:
        if len(username) != 0:
            flag = True
            for item in result:
                if item['Login'] == username:
                    cmd = 'sshpass -p %s ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no -o StrictHostKeyChecking=no %s@%s %s' % (result[0]['Password'], result[0]['Login'], host, ' '.join(str(param) for param in parameters) if parameters else '')
                    flag = False
            if flag:
                print('Found more than 1 item for host - {} and username {} not found among this items'.format(host, username))
                sys.exit(1)
        else:
            print('Found more than 1 item for host - {}'.format(host))
            sys.exit(1)
    os.system(cmd)


def create_cli():
    parser = argparse.ArgumentParser(description='ssh wrapper with teampass password manager integration')
    parser.add_argument('-s', '--server', type=str,
                        help='teampass api endpoint. environment variable TPSSH_ENDPOINT can be used',
                        default=os.environ.get('TPSSH_ENDPOINT', None))
    parser.add_argument('-t', '--token', type=str,
                        help='teampass api token. environment variable TPSSH_KEY can be used',
                        default=os.environ.get('TPSSH_KEY', None))
    parser.add_argument('host', type=str,
                        help='destination host. you can use the format username@host')
    parser.add_argument('params', type=list, nargs='*',
                        help='additional parameters for ssh command')
    return parser


def run():
    parser = create_cli()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    host = args.host.split('@')
    if len(host) == 1:
        username = ''
        host = host[0]
    elif len(host) == 2:
        username = host[0]
        host = host[1]
    else:
        print("Invalid destination host option format")
        sys.exit(1)
    set_proc_name(host.encode())
    spw(args.server, args.token, host, username, args.params)
