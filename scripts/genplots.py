#!/bin/python3

import argparse
import pandas as pd
import matplotlib.pyplot as plt


def main():
    df = pd.read_csv(args.csv_file)
    df = df.drop(columns=['run'], axis=0)

    df_seq = df[(df['access_type'] == 'seq_prefetch') | (df['access_type'] == 'seq') & (df['node_type'] == 'dram')]
    df_rnd = df[((df['access_type'] == 'rnd_prefetch') | (df['access_type'] == 'rnd')) & (df['node_type'] == 'dram')]
    df_pgn = df[(df['access_type'] == 'pgn_prefetch') | (df['access_type'] == 'pgn') & (df['node_type'] == 'dram')]

    # group = df_seq_prefetch.groupby(['node_type', 'access_type'], as_index=False)

    means = df_rnd.pivot_table('throughput', 'waitloop_iter', ['access_type', 'node_type'], aggfunc='mean')
    errors = df_rnd.pivot_table('throughput', 'waitloop_iter', ['access_type', 'node_type'], aggfunc='std')
    print(means)

    # means.plot(x='waitloop_iter', y='node_type', title='Sequential Access (prefetch)')
    means.plot()
    plt.show()



if __name__ == '__main__':
    pd.set_option('display.float_format', lambda x: '%.5f' % x)

    parser = argparse.ArgumentParser(description='Generate plots from YCSB and numastat csvs')
    parser.add_argument('--output-dir', '-o', dest='out_dir', default='figs', help='plots directory (default=./figs)')
    parser.add_argument('csv_file', action='store', help='CSV input file')
    args = parser.parse_args()
    main()
