#!/bin/python3

import argparse
import os
import warnings

import pandas as pd
import matplotlib.pyplot as plt


def plot_access(df, access_pattern, metric, node_type=None, logy=False, ymax=None):
    if node_type is None:
        df_loc = df[((df['access_pattern'] == f'{access_pattern}_prefetch') | (df['access_pattern'] == access_pattern))]
    else:
        df_loc = df[((df['access_pattern'] == f'{access_pattern}_prefetch') | (df['access_pattern'] == access_pattern))
                    & (df['node_type'] == node_type)]

    means = df_loc.pivot_table(metric, 'spinloop_iterations', ['access_pattern', 'node_kind'], aggfunc='mean')
    errors = df_loc.pivot_table(metric, 'spinloop_iterations', ['access_pattern', 'node_kind'], aggfunc='std')

    ymax = means.max().max() * 1.1 if ymax is None else ymax
    means.plot(style='.-', logy=logy, ylim=([0, ymax]))
    plt.title(f'{metric} for {access_pattern} access pattern')
    plt.savefig(f'{out_dir}/{access_pattern}_{metric}.jpeg')


def genplots(csv_file):
    df = pd.read_csv(csv_file)
    df = df.drop(columns=['run'], axis=0)

    patterns = ['seq', 'rnd', 'pgn']

    for p in patterns:
        plot_access(df, p, 'throughput', ymax=4e4)
        plot_access(df, p, 'cache_misses', ymax=1.8e8)


if __name__ == '__main__':
    pd.set_option('display.float_format', lambda x: '%.5f' % x)

    parser = argparse.ArgumentParser(description='Generate plots from YCSB and numastat csvs')
    parser.add_argument('--output-dir', '-o', dest='out_dir', default='figs', help='plots directory (default=./figs)')
    parser.add_argument('input', action='store', help='CSV input file/dir')
    args = parser.parse_args()

    test_name = os.path.basename(args.input).split('.')[0]
    out_dir = f'{args.out_dir}/{test_name}'
    os.makedirs(f'{out_dir}', exist_ok=True)

    print(f'Generating plots for {test_name}')
    genplots(args.input)
    print(f'Plots saved in {out_dir}')
