#!/bin/python3

import argparse
from os import access
import pandas as pd
import matplotlib.pyplot as plt


def main():
    df = pd.read_csv(args.csv_file)
    df = df.drop(columns=['run'], axis=0)
    # print(df)
   
    group = df.groupby(['node_type', 'access_type'], as_index=False)
    
    means = group.mean()
    errors = group.std()

    print(means.head(100))

    # means.plot(kind='bar', x='access_type', y='', grid=False, rot=0)
    # plt.show()



if __name__ == '__main__':
    pd.set_option('display.float_format', lambda x: '%.5f' % x)


    parser = argparse.ArgumentParser(
        description='Generate plots from YCSB and numastat csvs')
    parser.add_argument('--output-dir', '-o', dest='out_dir',
                        default='figs', help='plots directory (default=./figs)')
    parser.add_argument('csv_file', action='store', help='CSV input file')
    args = parser.parse_args()
    main()
