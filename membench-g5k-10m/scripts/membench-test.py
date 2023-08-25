#!/bin/python3

import argparse
import csv
import os
import shlex
import subprocess
import time
import math as m

# numa node, cpu node
DRAM = (0, 0)
PMEM = (3, 32)

PERF_EVENTS = [
    "cache-misses",
    "L1-dcache-load-misses",
    # "L1-dcache-loads",
    # "mem_load_retired.l1_miss",
    # "dTLB-load-misses",
    # "dTLB-store-misses",
    # "LLC-load-misses",
    # "LLC-loads",
    # "LLC-store-misses",
    # "LLC-stores",
    # "l1d.replacement",
    # "l1d_pend_miss.pending",
    # "l1d_pend_miss.pending_cycles",
    # "l1d_pend_miss.fb_full",
    # "sw_prefetch_access.nta",
    # "sw_prefetch_access.prefetchw",
    # "sw_prefetch_access.t0",
    # "sw_prefetch_access.t1_t2",
    # "branch-misses",
    # "branches",
    # "context-switches",
    # "cpu-cycles",
    # "instructions"
]


def is_event(string):
    for event in PERF_EVENTS:
        if event in string:
            return True
    return False


def is_counted(line):
    return '<not counted>' not in line


def extract_throughput(stdout):
    return stdout.decode('utf-8').strip()


def process_membench_stdout(stdout):
    output = stdout.decode('utf-8').strip().split(',')
    if len(output) == 1:
        return None, None
    throughput = output[0]
    sl_duration = output[1]
    return throughput, sl_duration


def extract_perf_results(perf_out):
    lines = perf_out.decode('utf-8').strip().split('\n')[2:]
    lines = filter(is_event, lines)
    lines = filter(is_counted, lines)
    table = [cols.strip().split() for cols in lines]
    return [val[0].strip().replace(',', '') for val in table]


def extract_sec_time_elapsed(perf_out):
    for line in perf_out.decode('utf-8').strip().split('\n'):
        if 'seconds time elapsed' in line:
            return line.split()[0]
    return


def run_membench(ex, flags, numa_node, cpu_node, iterations, n_operations):
    print(f"Running {ex} with flags {flags} on numa node {numa_node} and cpu node {cpu_node}, {iterations} it")
    event_str = ','.join(PERF_EVENTS)
    # c = f"numactl --membind={numa_node} --cpunodebind={cpu_node} perf stat -e {event_str} ./{args.build_dir}/{ex} " \
    #     f"-c -w {iterations} -o {n_operations} {flags}"
    c = f"numactl --membind={numa_node} --physcpubind={cpu_node} perf stat -e {event_str} ./{args.build_dir}/{ex} " \
        f"-c -w {iterations} -o {n_operations} {flags}"
    p = subprocess.run(shlex.split(c), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    throughput, sl_duration = process_membench_stdout(p.stdout)
    # print(p.stdout.decode())
    # print(p.stderr.decode())
    out_dict = {
        'throughput': throughput,
        'spinloop_duration': sl_duration,
        'seconds-time-elapsed': extract_sec_time_elapsed(p.stderr),
        **dict(zip(PERF_EVENTS, extract_perf_results(p.stderr)))
    }
    return out_dict


def benchmark_node(node_kind, iterations, n_ops):
    # print(f"Running benchmark on {node_kind} node")
    node = DRAM if node_kind == 'dram' else PMEM

    rows = list()
    rows.append({'node_kind': node_kind, 'access_pattern': 'seq', 'spinloop_iterations': iterations,
                 **run_membench('membench', '-s', node[0], node[1], iterations, n_ops)})
    rows.append({'node_kind': node_kind, 'access_pattern': 'pgn', 'spinloop_iterations': iterations,
                 **run_membench('membench', '-g', node[0], node[1], iterations, n_ops)})
    rows.append({'node_kind': node_kind, 'access_pattern': 'rnd', 'spinloop_iterations': iterations,
                 **run_membench('membench', '-r', node[0], node[1], iterations, n_ops)})
    rows.append({'node_kind': node_kind, 'access_pattern': 'seq_prefetch', 'spinloop_iterations': iterations,
                 **run_membench('membench', '-s -p', node[0], node[1], iterations, n_ops)})
    rows.append({'node_kind': node_kind, 'access_pattern': 'pgn_prefetch', 'spinloop_iterations': iterations,
                 **run_membench('membench', '-g -p', node[0], node[1], iterations, n_ops)})
    rows.append({'node_kind': node_kind, 'access_pattern': 'rnd_prefetch', 'spinloop_iterations': iterations,
                 **run_membench('membench', '-r -p', node[0], node[1], iterations, n_ops)})
    return rows


def benchmark_node_baseline(node_kind, ex):
    node = DRAM if node_kind == 'dram' else PMEM
    return {'node_kind': node_kind, 'exec': ex, **run_membench(ex, '', node[0], node[1], 0, 0)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run membench test')
    parser.add_argument('test_name', action='store', help='Name of the test')
    parser.add_argument('--n-runs', '-n', dest='n_runs', default=1, help='Number of runs (default=1)')
    parser.add_argument('--build-dir', '-b', dest='build_dir', default='build',
                        help='CMake build directory (default=build)')
    parser.add_argument('--dram-only', '-d', dest='dram_only', action='store_true', default=False,
                        help='Only benchmark DRAM')

    args = parser.parse_args()

    if not args.dram_only:
        PERF_EVENTS = PERF_EVENTS + [
            "mem_load_retired.l3_miss",
            "mem_load_l3_miss_retired.local_dram",
            "mem_load_retired.local_pmm"
        ]

    n_operations = [100_000_000]
    compiler_flags = [
        '-O3',
        '-O0'
    ]
    spinloop_iterations = [
        0,
        # 500,
        # 1_000,
        # 1_500,
        # 2_000,
        2_500,
        # 3_000,
        # 3_500,
        # 4_000,
        # 4_500,
        5_000,
        # 10_000,
        20_000,
        # 30_000,
        # 40_000,
        # 50_000,
        # 100_000,
        # 500_000,
        # 750_000,
    ]

    runs = range(1, int(args.n_runs) + 1)
    os.makedirs('logs', exist_ok=True)
    exp_time = time.time()
    for n in n_operations:
        print(f"Running benchmark with {n} operations")

        for flag in compiler_flags:
            print(f"--- Running baseline with flag {flag} ---")
            if n == 0:
                filename = f'logs/{args.test_name}_0_{flag[1:]}.csv'
            else:
                filename = f'logs/{args.test_name}_{int(n / 1_000_000)}M_{flag[1:]}.csv'
            f = open(filename, 'w')

            fieldnames = ['exec', 'run', 'node_kind', 'access_pattern', 'spinloop_iterations', 'throughput',
                          'seconds-time-elapsed', 'spinloop_duration', *PERF_EVENTS]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            # clean and build
            subprocess.run(shlex.split('make clean --directory build'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(shlex.split(f'cmake -B build -DCMAKE_C_FLAGS="{flag}"'))
            subprocess.run(shlex.split('make --directory build'))

            for r in runs:
                t_start = time.time()
                print(f'--- Run {r} ---')

                print('-> Baseline tests ')
                writer.writerow({'run': r, **benchmark_node_baseline('dram', 'membench_base')})
                writer.writerow({'run': r, **benchmark_node_baseline('dram', 'membench_data_init')})
                writer.writerow({'run': r, **benchmark_node_baseline('dram', 'membench_pregen_init')})

                if not args.dram_only:
                    writer.writerow({'run': r, **benchmark_node_baseline('pmem', 'membench_base')})
                    writer.writerow({'run': r, **benchmark_node_baseline('pmem', 'membench_data_init')})
                    writer.writerow({'run': r, **benchmark_node_baseline('pmem', 'membench_pregen_init')})

                f.flush()

                print(f'-> Membench tests')
                for w in spinloop_iterations:
                    for row in benchmark_node('dram', w, n):
                        writer.writerow({'exec': 'membench', 'run': r, **row})
                    if not args.dram_only:
                        for row in benchmark_node('pmem', w, n):
                            writer.writerow({'exec': 'membench', 'run': r, **row})
                    f.flush()
                run_time = time.time() - t_start
                # print runtime in hours
                print(f'--- Run {r} took {m.ceil(run_time / 3600)} hours for flag {flag} ---')

            f.close()

    print(f'--- Experiment took {m.ceil((time.time() - exp_time) / 3600)} hours ---')
