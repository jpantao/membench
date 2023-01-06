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
        bins = df['count'].unique()
        df.hist(column=['count'], grid=True, bins=24)
        plt.title(f'{exe} - Random generation distribution')
        plt.xticks(bins)
        plt.savefig(f'figs/{exe}.png')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate from rand results')
    args = parser.parse_args()

    print('--- Generating logs ---')
    gen_logs()
    print('--- Generating plots ---')
    gen_plots()
    print('--- Done ---')
