#!/bin/python3

import argparse
import os

import pandas as pd
import matplotlib.pyplot as plt

METRICS = [
    "throughput",
    "seconds-time-elapsed",
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


def plot_access(data, access_pattern, metric, node_type=None, logy=False, ymax=None):
    if node_type is None:
        df_loc = data[
            ((data['access_pattern'] == f'{access_pattern}_prefetch') | (data['access_pattern'] == access_pattern))
            & (data['exec'] == 'membench')]
    else:
        df_loc = data[
            ((data['access_pattern'] == f'{access_pattern}_prefetch') | (data['access_pattern'] == access_pattern))
            & (data['exec'] == 'membench') & (data['node_type'] == node_type)]

    means = df_loc.pivot_table(metric, 'spinloop_iterations', ['access_pattern', 'node_kind'], aggfunc='mean')
    errors = df_loc.pivot_table(metric, 'spinloop_iterations', ['access_pattern', 'node_kind'], aggfunc='std')

    # print(means)
    # ymax = means.max().max() * 1.5 if ymax is None else ymax
    # print(means.max())
    # print(means.max().max())
    # means.plot(style='.-', logy=logy, ylim=([0, ymax]))

    if ymax is None:
        means.plot(style='.-', logy=logy)
    else:
        means.plot(style='.-', logy=logy, ylim=([0, ymax]))

    # plt.ticklabel_format(style='plain', axis='y')
    plt.title(f'{metric} for {access_pattern} access pattern')
    plt.savefig(f'{out_dir}/spinloop_{access_pattern}_{metric}.jpeg')


def gen_spinloop_plots(data):
    print('--- Spinloop plots ---')
    patterns = ['seq', 'rnd', 'pgn']

    for m in METRICS:
        print(m)
        for p in patterns:
            if m == 'throughput':
                plot_access(data, p, m, ymax=50000)
            else:
                plot_access(data, p, m)


def gen_baseline_plots(data):
    print('--- Baseline plots ---')
    baselines = data[((data['exec'] == 'membench_base')
                      | (data['exec'] == 'membench_data_init')
                      | (data['exec'] == 'membench_pregen_init'))]
    baselines = baselines.drop(columns=['access_pattern', 'spinloop_iterations', 'throughput'], axis=0)

    for m in METRICS:
        if m == 'throughput':
            continue
        print(m)
        means = baselines.pivot_table(m, 'exec', ['node_kind'], aggfunc='mean')
        errors = baselines.pivot_table(m, 'exec', ['node_kind'], aggfunc='std')
        means.plot.bar(rot=0, yerr=errors)
        plt.title(f'Baseline for {m}')
        plt.savefig(f'{out_dir}/baseline_{m}.jpeg')


if __name__ == '__main__':
    plt.rcParams.update({'figure.max_open_warning': 0})
    pd.set_option('display.float_format', lambda x: '%.5f' % x)

    parser = argparse.ArgumentParser(description='Generate from membench results')
    parser.add_argument('input', action='store', help='CSV input file/dir')
    args = parser.parse_args()

    test_name = os.path.basename(args.input).split('.')[0]
    out_dir = f'figs/{test_name}'
    os.makedirs(f'{out_dir}', exist_ok=True)

    df = pd.read_csv(args.input)
    df = df.drop(columns=['run'], axis=0)

    print(f'Generating plots for {test_name}')
    gen_spinloop_plots(df)
    gen_baseline_plots(df)
    print(f'Plots saved in logs')
