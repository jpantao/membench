#!/bin/python3

import argparse
import pandas as pd
import matplotlib.pyplot as plt


def main():
    df = pd.read_csv(args.csv_file)
    df = df.drop(columns=['run'], axis=0)
    # print(df)
   
    cm = df.drop(columns=['throughput'], axis=0).groupby(['node_type', 'access_type'])
    cm_means = cm.mean()
    cm_errors = cm.std()
    # print(cm_means.head(100))
    # print(cm.groups)
    
    # test = df.loc[cm.groups['dram']]
    # print(test)


    group = df.groupby(['node_type', 'access_type'], as_index=False)
    means = group.mean()
    errors = group.std()
    print(means.head(100))

    # means.plot(kind='bar', x='access_type', y='cache_misses', grid=False, rot=0)
    plt.show()



if __name__ == '__main__':
    pd.set_option('display.float_format', lambda x: '%.5f' % x)


    parser = argparse.ArgumentParser(
        description='Generate plots from YCSB and numastat csvs')
    parser.add_argument('--output-dir', '-o', dest='out_dir',
                        default='figs', help='plots directory (default=./figs)')
    parser.add_argument('csv_file', action='store', help='CSV input file')
    args = parser.parse_args()
    main()
