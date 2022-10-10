#!/bin/bash

# usage:
# ./scripts/bennchmark-node.sh <numa_node> <node_type> <log_file> <run_n>

numa_node=$1 
node_type=$2
log_file=$3
run_n=$4

# echo "run,node_type,access_type,throughput,cache_misses" | tee -a ${log_file}
echo "${run_n},${node_type},seq,$(numactl --membind=${numa_node} ./membench -c -s)" | tee -a ${log_file}
echo "${run_n},${node_type},rnd,$(numactl --membind=${numa_node} ./membench -c -r)" | tee -a ${log_file}
echo "${run_n},${node_type},pgn,$(numactl --membind=${numa_node} ./membench -c -g)" | tee -a ${log_file}
echo "${run_n},${node_type},seq_prefetch,$(numactl --membind=${numa_node} ./membench -c -s -p)" | tee -a ${log_file}
echo "${run_n},${node_type},rnd_prefetch,$(numactl --membind=${numa_node} ./membench -c -r -p)" | tee -a ${log_file}
echo "${run_n},${node_type},pgn_prefetch,$(numactl --membind=${numa_node} ./membench -c -g -p)" | tee -a ${log_file}
