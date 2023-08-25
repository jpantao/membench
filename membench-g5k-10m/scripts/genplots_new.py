#!/bin/python3

import os
import argparse
import subprocess
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.container import ErrorbarContainer
from matplotlib.ticker import FuncFormatter

metrics = {
    "throughput": [0, 70],
    "cache-misses": [100, 110],
    "L1-dcache-load-misses": [165, 190],
    # "l1d.replacement": [None, None],
    # "LLC-load-misses": [None, None],
    # "LLC-store-misses": [None, None],
    # "dTLB-load-misses": [None, None],
    # "dTLB-store-misses": [None, None],
}

color_map = {
    "dram": "blue",
    "dram_prefetch": "steelblue",
    "pmem": "darkorange",
    "pmem_prefetch": "goldenrod",
}

line_styles = ['x-', 'x--', 'x-.', 'x:']

prefetch_suffix = '_prefetch'
plot_extension = 'pdf'


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
    df_b = df[((df['exec'] == 'base')
               | (df['exec'] == 'data_init')
               | (df['exec'] == 'pregen_init'))]

    for m in metrics:
        if m == 'throughput':
            continue
        print(f'Plotting {m}')

        means = df_b.pivot_table(m, 'exec', ['node_kind'], aggfunc='mean')
        stdev = df_b.pivot_table(m, 'exec', ['node_kind'], aggfunc='std')
        colors = gen_colors(means.columns)

        ax = means.plot.bar(yerr=stdev, capsize=4, rot=0, ylim=[0, 100], color=colors)
        add_bar_labels(ax)
        # add_errorbar_labels(ax, stdev)
        # addlabels(stdev.values.flatten())
        # plt.title(f'Baseline for {m}')
        plt.ylabel(f'Count (millions of events)')
        plt.xlabel('')
        plt.legend(fontsize="medium", loc='upper left')
        plt.savefig(f'{out_dir}/{out_dir.split("/")[1]}_baseline_{m}.{plot_extension}', bbox_inches='tight')
        exec_epspdf(f'{out_dir}/{out_dir.split("/")[1]}_baseline_{m}.{plot_extension}')
        # plt.show()
        plt.close()


def add_bar_labels(ax):
    for container in ax.containers:
        if isinstance(container, ErrorbarContainer):
            continue
        ax.bar_label(container, labels=[f'{x:,.2f}M' for x in container.datavalues], rotation=45, padding=3)


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

        means.plot(style=line_styles, rot=0, ylim=metrics[m], color=colors)
        # plt.title(f'{m} for {p} access pattern')
        if m == 'throughput':
            plt.ylabel(f'Throughput (Kops/s)')
        else:
            plt.ylabel(f'Count (millions of events)')
        plt.xlabel('Spinloop duration (\u03BCs)')

        if p == 'seq' and m == 'throughput':
            plt.legend(fontsize="small", loc='lower right')
        elif p == 'seq':
            plt.legend(fontsize="small", loc='upper left')
        else:
            # remove legend
            plt.gca().get_legend().remove()

        plt.savefig(f'{out_dir}/{out_dir.split("/")[1]}_spinloop_{p}_{m}.{plot_extension}', bbox_inches='tight')
        exec_epspdf(f'{out_dir}/{out_dir.split("/")[1]}_spinloop_{p}_{m}.{plot_extension}')
        # plt.show()
        plt.close()


def exec_epspdf(filename):
    subprocess.run(['epspdf', '-b', filename], stdout=subprocess.DEVNULL)
    subprocess.run(['rm', f'{filename}.backup'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate from membench results')
    parser.add_argument('input', action='store', help='CSV input file')

    # Set font and font size for all text elements in the plot
    plt.rcParams['font.family'] = 'Sans Serif'  # Change to the font family you desire (e.g., 'sans-serif', 'monospace')
    plt.rcParams['font.size'] = 18  # Change to the desired font size

    args = parser.parse_args()

    test_name = os.path.basename(args.input).split('.')[0]
    print('-' * 80)
    print(f'Generating plots for {test_name}')
    out_dir = f'figs/{test_name}'
    os.makedirs(f'{out_dir}', exist_ok=True)

    df = pd.read_csv(args.input)
    df = df.drop(columns=['run'], axis=0)

    # convert spinloop_duration from ms to us
    df['spinloop_duration'] = df['spinloop_duration'] * 1000
    # convert throughput from ops/s to Kops/s
    df['throughput'] = df['throughput'] / 1000
    # convert L1-dcache-load-misses to M
    df['L1-dcache-load-misses'] = df['L1-dcache-load-misses'] / 1_000_000
    # convert cache-misses to M
    df['cache-misses'] = df['cache-misses'] / 1_000_000

    # remove 'membench_' prefix from exec
    df['exec'] = df['exec'].str.replace('membench_', '')

    genplot_baseline()
    genplot_bench()
    print('-' * 80)
