#!/bin/python3

import os
import paramiko
import argparse
import subprocess


def get_reservation_node():
    print("Getting reservation node")
    filename = os.getenv('OAR_NODE_FILE')
    if filename is None:
        print('No node found in OAR_NODE_FILE')
        exit(1)
    with open(filename) as f:
        return f.readline().strip()


def paramiko_connect(node, user):
    print("Connecting to node")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(node, username=user)
    return ssh


def paramiko_exec(ssh, cmd):
    print(f'Executing command: {cmd}')
    stdin, stdout, stderr = ssh.exec_command(cmd)
    return stdout.readlines()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Deploy membench test')
    parser.add_argument('--n-runs', '-n', dest='n_runs', default=1, help='Number of runs (default=1)')
    parser.add_argument('test_name', action='store', help='Name of the test')
    args = parser.parse_args()

    # kadeploy
    subprocess.run(["scripts/deploy.sh"])

    hostname = get_reservation_node()
    host = paramiko_connect(hostname, os.getenv('USER'))
    paramiko_exec(host, f'cd {os.getcwd()} && ./scripts/membench-test.py {args.test_name} -n {args.n_runs}')
