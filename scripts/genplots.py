#!/bin/python3

import argparse
import os

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.container import ErrorbarContainer

METRICS = [
    "throughput",
    # "seconds-time-elapsed",
    "cache-misses",
    "L1-dcache-load-misses",
    # "L1-dcache-loads",
    # "LLC-load-misses",
    # "LLC-loads",
    # "LLC-store-misses",
    # "LLC-stores",
    # "l1d_pend_miss.pending",
    # "l1d_pend_miss.pending_cycles",
    # "l1d.replacement",
    # "l1d_pend_miss.fb_full",
    # "sw_prefetch_access.nta",
    # "sw_prefetch_access.prefetchw",
    # "sw_prefetch_access.t0",
    # "sw_prefetch_access.t1_t2",
    # "context-switches",
    # "branch-misses",
    # "branches",
    # "cpu-cycles",
    # "instructions",
    # "mem_load_retired.l3_miss",
    # "mem_load_l3_miss_retired.local_dram",
    # "mem_load_retired.local_pmm"
]

YMAX = {
    "throughput": [0, 70000],
    "seconds-time-elapsed": [None, 200],
    "cache-misses": [None, 4e8],
    "L1-dcache-load-misses": [1.6e8, 1.9e8],
    "L1-dcache-loads": [None, 9e9],
    "LLC-load-misses": [None, 4e8],
    "LLC-loads": None,
    "LLC-store-misses": [None, 4e8],
    "LLC-stores": None,
    "l1d_pend_miss.pending": [None, 1.75e11],
    "l1d_pend_miss.pending_cycles": [None, 1.75e11],
    "l1d.replacement": None,
    "l1d_pend_miss.fb_full": None,
    "sw_prefetch_access.nta": [None, 1.2e8],
    "sw_prefetch_access.prefetchw": None,
    "sw_prefetch_access.t0": None,
    "sw_prefetch_access.t1_t2": None,
    "branch-misses": [None, 2e9],
    "context-switches": None,
    "branches": [None, 2e9],
    "cpu-cycles": None,
    "instructions": None,
    # "mem_load_retired.l3_miss": None,
    # "mem_load_l3_miss_retired.local_dram": None,
    # "mem_load_retired.local_pmm": None
}

ROTATION = {
    "throughput": 90,
    "seconds-time-elapsed": 90,
    "cache-misses": 90,
    "L1-dcache-load-misses": 90,
    "L1-dcache-loads": 90,
    "LLC-load-misses": 90,
    "LLC-loads": 90,
    "LLC-store-misses": 90,
    "LLC-stores": 90,
    "l1d_pend_miss.pending": 90,
    "l1d_pend_miss.pending_cycles": 90,
    "l1d.replacement": 90,
    "l1d_pend_miss.fb_full": 90,
    "sw_prefetch_access.nta": 90,
    "sw_prefetch_access.prefetchw": 90,
    "sw_prefetch_access.t0": 90,
    "sw_prefetch_access.t1_t2": 90,
    "context-switches": None,
    "branch-misses": 90,
    "branches": 90,
    "cpu-cycles": 90,
    "instructions": 90,
    # "mem_load_retired.l3_miss": 90,
    # "mem_load_l3_miss_retired.local_dram": 90,
    # "mem_load_retired.local_pmm": 90
}


def plot_access(data, access_pattern, metric, node_type=None, logy=False, ymax=None):
    if node_type is None:
        df_loc = data[
            ((data['access_pattern'] == f'{access_pattern}_prefetch') | (data['access_pattern'] == access_pattern))
            & (data['exec'] == 'membench')]
    else:
        df_loc = data[
            ((data['access_pattern'] == f'{access_pattern}_prefetch') | (data['access_pattern'] == access_pattern))
            & (data['exec'] == 'membench') & (data['node_type'] == node_type)]
    # print(df_loc)
    means = df_loc.pivot_table(metric, 'spinloop_iterations', ['access_pattern', 'node_kind'], aggfunc='mean')
    errors = df_loc.pivot_table(metric, 'spinloop_iterations', ['access_pattern', 'node_kind'], aggfunc='std')

    # map spinloop_iterations to spinloop_duration ignoring access_pattern and node_kind
    spinloop_duration = df_loc.pivot_table('spinloop_duration', 'spinloop_iterations', [], aggfunc='mean')

    # errors = df_loc.pivot_table(metric, 'spinloop_duration', ['access_pattern', 'node_kind'], aggfunc='std')

    # print(spinloop_duration)

    # plot means with spinloop_duration as x-axis
    means.index = spinloop_duration['spinloop_duration']
    # print(means)

    if ymax is None:
        means.plot(style='.-', logy=logy)
    else:
        means.plot(style='.-', logy=logy, ylim=ymax)

    # plt.ticklabel_format(style='plain', axis='y')
    plt.title(f'{metric} for {access_pattern} access pattern')
    plt.savefig(f'{out_dir}/{out_dir.split("/")[1]}_spinloop_{access_pattern}_{metric}.pdf')
    # plt.show()


def gen_spinloop_plots(data):
    print('--- Spinloop plots ---')
    patterns = ['seq', 'rnd', 'pgn']

    for m in METRICS:
        # print(m)
        for p in patterns:
            plot_access(data, p, m, ymax=YMAX[m])


def gen_baseline_plots(data):
    print('--- Baseline plots ---')
    baselines = data[((data['exec'] == 'membench_base')
                      | (data['exec'] == 'membench_data_init')
                      | (data['exec'] == 'membench_pregen_init'))]
    baselines = baselines.drop(columns=['access_pattern', 'spinloop_iterations', 'throughput'], axis=0)
    for m in METRICS:
        if m == 'throughput':
            continue
        # print(m)

        means = baselines.pivot_table(m, 'exec', ['node_kind'], aggfunc='mean')
        errors = baselines.pivot_table(m, 'exec', ['node_kind'], aggfunc='std')
        if YMAX[m] is None:
            ax = means.plot.bar(rot=0, yerr=errors)
        else:
            ax = means.plot.bar(rot=0, yerr=errors, ylim=([None, YMAX[m][1]]))
        plt.legend(loc='upper left')
        for container in ax.containers:
            if isinstance(container, ErrorbarContainer):
                continue
            ax.bar_label(container, labels=[f'{x:,.0f}' for x in container.datavalues], rotation=ROTATION[m], padding=3)
        plt.title(f'Baseline for {m}')
        plt.savefig(f'{out_dir}/{out_dir.split("/")[1]}_baseline_{m}.pdf')


if __name__ == '__main__':
    plt.rcParams.update({'figure.max_open_warning': 0})
    # pd.set_option('display.float_format', lambda x: '%.5f' % x)

    parser = argparse.ArgumentParser(description='Generate from membench results')
    parser.add_argument('input', action='store', help='CSV input file/dir')
    args = parser.parse_args()

    test_name = os.path.basename(args.input).split('.')[0]
    out_dir = f'figs/{test_name}'
    os.makedirs(f'{out_dir}', exist_ok=True)

    df = pd.read_csv(args.input)
    df = df.drop(columns=['run'], axis=0)

    print(f'Generating plots for {test_name}')
    gen_baseline_plots(df)
    gen_spinloop_plots(df)
    cache_misses = df['cache-misses'].mean()
    print(f'Average cache misses:\t{round(cache_misses / 1000000, 2)}M')
    l1_misses = df['L1-dcache-load-misses'].mean()
    print(f'Average L1 misses:\t{round(l1_misses / 1000000, 2)}M')
    print(f'Plots saved in figs')
    print('')
