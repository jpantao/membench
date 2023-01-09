#!/bin/python3


import argparse
import pandas as pd
import matplotlib.pyplot as plt
import os
import subprocess
import shlex

execs = ['membench_randr', 'membench_lehmer', 'membench_wyhash']


def gen_logs():
    # clean and build
    subprocess.run(shlex.split('cmake -B build'))
    subprocess.run(shlex.split('make clean --directory build'))
    subprocess.run(shlex.split('make --directory build'))

    for exe in execs:
        print(f'Generating logs for {exe}')
        cmd = f'./build/{exe} > ./logs/{exe}.csv'
        with open(f'./logs/{exe}.csv', 'w') as log:
            subprocess.run(shlex.split(cmd), stdout=log)


def gen_plots():
    for exe in execs:
        print(f'Generating plots for {exe}')
        df = pd.read_csv(f'logs/{exe}.csv', dtype={'val': 'str', 'count': int})
        df = df.groupby(['val']).sum()
        print(f'Number unique values: {len(df)}')
        bins = range(0, 25, 1)
        df.hist(column=['count'], grid=True, bins=bins, rwidth=0.9, color='#607c8e')
        plt.title(f'{exe.split("_")[1]} - Random generation distribution')
        plt.xticks(bins)
        plt.savefig(f'figs/{exe}.png')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate from rand results')
    parser.add_argument('--only-plots', '-p', dest='only_plots', action='store_true', default=False, help='only plots')
    args = parser.parse_args()

    if not args.only_plots:
        print('--- Generating logs ---')
        gen_logs()

    print('--- Generating plots ---')
    gen_plots()

    print('--- Done ---')
