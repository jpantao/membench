#!/bin/python3

import argparse
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run membench test')
    parser.add_argument('--n-runs', '-n', dest='n_runs', default=3, help='Number of runs (default=3)')
    parser.add_argument('test_name', action='store', help='Name of the test')
    args = parser.parse_args()


