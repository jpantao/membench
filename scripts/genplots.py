#!/bin/python3

import argparse
import os

import pandas as pd
import matplotlib.pyplot as plt


def plot_access(df, access_pattern, metric, node_type=None):
    if node_type is None:
        df_loc = df[((df['access_type'] == f'{access_pattern}_prefetch') | (df['access_type'] == access_pattern))]
    else:
        df_loc = df[((df['access_type'] == f'{access_pattern}_prefetch') | (df['access_type'] == access_pattern)) & (
                df['node_type'] == node_type)]

    means = df_loc.pivot_table(metric, 'waitloop_iter', ['access_type', 'node_type'], aggfunc='mean')
    errors = df_loc.pivot_table(metric, 'waitloop_iter', ['access_type', 'node_type'], aggfunc='std')
    means.plot(style='.-')
    plt.savefig(f'figs/{access_pattern}_{metric}.jpeg')


def main():
    df = pd.read_csv(args.csv_file)
    df = df.drop(columns=['run'], axis=0)

    patterns = ['seq', 'rnd', 'pgn']

    for p in patterns:
        plot_access(df, p, 'throughput')
        plot_access(df, p, 'cache_misses')

    plt.show()


if __name__ == '__main__':
    pd.set_option('display.float_format', lambda x: '%.5f' % x)

    parser = argparse.ArgumentParser(description='Generate plots from YCSB and numastat csvs')
    parser.add_argument('--output-dir', '-o', dest='out_dir', default='figs', help='plots directory (default=./figs)')
    parser.add_argument('csv_file', action='store', help='CSV input file')
    args = parser.parse_args()
    os.makedirs('figs', exist_ok=True)
    main()
