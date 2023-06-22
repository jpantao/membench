#!/bin/python3

import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt

metrics = {
    "throughput": [0, 70000],
    "cache-misses": [1e8, 1.1e8],
    "L1-dcache-load-misses": [1.6e8, 1.9e8],
    "l1d.replacement": [1.6e8, 1.9e8],
    "LLC-load-misses": None,
    "LLC-store-misses": None,
    "dTLB-load-misses": None,
    "dTLB-store-misses": None
}


def genplot_baseline(df):
    pass


def genplot_bench(df):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate from membench results')
    parser.add_argument('input', action='store', help='CSV input file')
    args = parser.parse_args()

    test_name = os.path.basename(args.input).split('.')[0]
    out_dir = f'figs/{test_name}'
    os.makedirs(f'{out_dir}', exist_ok=True)

    df = pd.read_csv(args.input)
    print('-' * 100)
    print(df)
    print('-' * 100)
    # drop run column and pivot by average and stddev
    df = df.drop(columns=['run'], axis=0)

    # drop columns not in metrics
    # cols = ['exec', 'node_kind', 'access_pattern', 'spinloop_iterations', *metrics.keys()]
    # print(cols)
    # df = df.drop(columns=[c for c in df.columns if c not in cols], axis=0)

    means = df.pivot_table(index=['exec', 'node_kind', 'access_pattern', 'spinloop_iterations'], aggfunc='mean')
    errors = df.pivot_table(index=['exec', 'node_kind', 'access_pattern', 'spinloop_iterations'], aggfunc='std')

    print(means)
    print('-' * 100)
    print(errors)
    print('-' * 100)
