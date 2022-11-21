#!/bin/python3

import os
import paramiko
import argparse
import subprocess

PERF_EVENTS = [
    "cache-misses",
    "L1-dcache-load-misses",
    "L1-dcache-loads",
    "LLC-load-misses",
    "LLC-loads",
    "LLC-store-misses",
    "LLC-stores",
    "l1d_pend_miss.pending",
    "l1d_pend_miss.pending_cycles",
    "l1d.replacement",
    "l1d_pend_miss.fb_full",
    "sw_prefetch_access.nta",
    "sw_prefetch_access.prefetchw",
    "sw_prefetch_access.t0",
    "sw_prefetch_access.t1_t2",
    "branch-misses",
    "branches",
    "cpu-cycles",
    "instructions"
]


def deploy_kadeploy_img():
    print("Deploying reservation")
    subprocess.run(["scripts/deploy.sh"])
    return get_reservation_node()


def get_reservation_node():
    print("Getting reservation node")
    with open(os.getenv('OAR_NODE_FILE')) as f:
        return f.readline().strip()


def paramiko_connect(node, user):
    print("Connecting to node")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(node, username=user)
    return ssh


def paramiko_exec(ssh, cmd):
    print(f"Executing command: {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    return stdout.readlines()


def run_test(n_runs, out_csv):
    print("Running test")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Deploy membench test')
    parser.add_argument('--n-runs', '-n', dest='n_runs', default=3, help='Number of runs (default=3)')
    parser.add_argument('test_name', action='store', help='Name of the test')
    args = parser.parse_args()

    out = f'logs/{args.test_name}.log'

    hostname = deploy_kadeploy_img()
    host = paramiko_connect(hostname, os.getenv('USER'))
    paramiko_exec(host, f"scripts/run-test.sh {args.n_runs} {out}")
