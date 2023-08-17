#!/bin/python3

import os
import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.container import ErrorbarContainer

metrics = {
    "throughput": [0, 70000],
    "cache-misses": [1e8, 1.1e8],
    "L1-dcache-load-misses": [1.6e8, 1.9e8],
    "l1d.replacement": [1.6e8, 1.9e8],
    "LLC-load-misses": [None, None],
    "LLC-store-misses": [None, None],
    "dTLB-load-misses": [None, None],
    "dTLB-store-misses": [None, None],
}

# spinloop
# metrics = {
#     "throughput": [0, 70000],
#     "cache-misses": [0, 0.05e8],
#     "L1-dcache-load-misses": [0.6e8, 0.8e8],
#     "l1d.replacement": [0.6e8, 0.8e8],
#     "LLC-load-misses": [None, None],
#     "LLC-store-misses": [None, None],
#     "dTLB-load-misses": [None, None],
#     "dTLB-store-misses": [None, None],
# }

# metrics = {
#     "throughput": [None, None],
#     "cache-misses": [None, None],
#     "L1-dcache-load-misses": [None, None],
#     "l1d.replacement": [None, None],
#     "LLC-load-misses": [None, None],
#     "LLC-store-misses": [None, None],
#     "dTLB-load-misses": [None, None],
#     "dTLB-store-misses": [None, None],
# }


color_map = {
    "dram": "blue",
    "dram_prefetch": "steelblue",
    "pmem": "darkorange",
    "pmem_prefetch": "goldenrod",
}

prefetch_suffix = '_prefetch'
plot_extension = 'png'


def get_value_by_partial_key(dictionary, partial_key, default=None):
    for key in dictionary.keys():
        if partial_key in key:
            return dictionary[key]
    return default


def gen_colors(config_list):
    # create a color list based on the config_list using the color_map
    default_colors = sns.color_palette("hls", len(config_list))  # create a color palette (orange to blue)
    default_colors.reverse()  # just to make the plots pretty (from blue to orange)
    colors = [color_map.get(config, color) for config, color in zip(config_list, default_colors)]
    return colors


def genplot_baseline():
    print('genplot_baseline')

    # select only the baseline data
    df_b = df[((df['exec'] == 'membench_base')
               | (df['exec'] == 'membench_data_init')
               | (df['exec'] == 'membench_pregen_init'))]

    for m in metrics:
        if m == 'throughput':
            continue
        print(f'Plotting {m}')

        means = df_b.pivot_table(m, 'exec', ['node_kind'], aggfunc='mean')
        stdev = df_b.pivot_table(m, 'exec', ['node_kind'], aggfunc='std')
        colors = gen_colors(means.columns)

        ax = means.plot.bar(yerr=stdev, capsize=4, rot=0, ylim=[0, 1e8], color=colors)
        add_bar_labels(ax)
        # add_errorbar_labels(ax, stdev)
        # addlabels(stdev.values.flatten())
        plt.title(f'Baseline for {m}')
        plt.savefig(f'{out_dir}/{out_dir.split("/")[1]}_baseline_{m}.{plot_extension}')
        # plt.show()
        plt.close()


def add_bar_labels(ax):
    for container in ax.containers:
        if isinstance(container, ErrorbarContainer):
            continue
        ax.bar_label(container, labels=[f'{x:,.2e}' for x in container.datavalues], rotation=45, padding=3)

def add_errorbar_labels(ax, stddev):
    for container in ax.containers:
        if isinstance(container, ErrorbarContainer):
            print('-----------')
            print(container)
            print('-----------')
            continue
        print(container.datavalues)
        print(stddev)



def genplot_bench():
    print('genplot_bench')

    # select only the benchmark data
    df_b = df[(df['exec'] == 'membench')]

    # select patterns removing tailing _prefetch
    patterns = df_b['access_pattern'].str.replace(prefetch_suffix, '').unique()

    plots = [(m, p) for m in metrics for p in patterns]

    for m, p in plots:
        print(f'Plotting {m} {p}')
        df_p = df_b[((df_b['access_pattern'] == f'{p}_prefetch') | (df_b['access_pattern'] == p))]
        means = df_p.pivot_table(m, 'spinloop_iterations', ['access_pattern', 'node_kind'], aggfunc='mean')
        # map spinloop_iterations to spinloop_duration ignoring access_pattern and node_kind
        spinloop_duration = df_p.pivot_table('spinloop_duration', 'spinloop_iterations', [], aggfunc='mean')
        means.index = spinloop_duration['spinloop_duration']

        columns = [f'{t[1]}{prefetch_suffix}' if prefetch_suffix in t[0] else t[1] for t in means.columns]
        colors = gen_colors(columns)

        means.plot(style='.-', rot=0, ylim=metrics[m], color=colors)
        plt.title(f'{m} for {p} access pattern')
        plt.savefig(f'{out_dir}/{out_dir.split("/")[1]}_spinloop_{p}_{m}.png')
        # plt.show()
        plt.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate from membench results')
    parser.add_argument('input', action='store', help='CSV input file')
    args = parser.parse_args()

    test_name = os.path.basename(args.input).split('.')[0]
    print('-' * 80)
    print(f'Generating plots for {test_name}')
    out_dir = f'figs/{test_name}'
    os.makedirs(f'{out_dir}', exist_ok=True)

    df = pd.read_csv(args.input)
    df = df.drop(columns=['run'], axis=0)

    genplot_baseline()
    genplot_bench()
    print('-' * 80)
