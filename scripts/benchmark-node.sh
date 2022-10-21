#!/bin/bash

# usage:
# ./scripts/bennchmark-node.sh <numa_node> <node_type> <log_file> <run_n>

numa_node=$1 
node_type=$2
perf_event=$3
log_file=$4
run_n=$5

# echo "run,node_type,access_type,throughput,cache_misses" | tee -a ${log_file}
echo -n "${run_n},${node_type},seq,$(perf record -e ${perf_event} numactl --membind=${numa_node} ./membench -c -s 2>/dev/null)" | tee -a ${log_file}
echo "perf report --header | egrep Event | sed 's/^.*: //'" | tee -a ${log_file}
rm perf.data
echo -n "${run_n},${node_type},rnd,$(perf record -e ${perf_event} numactl --membind=${numa_node} ./membench -c -r 2>/dev/null)" | tee -a ${log_file}
echo "perf report --header | egrep Event | sed 's/^.*: //'" | tee -a ${log_file}
rm perf.data
echo -n "${run_n},${node_type},pgn,$(perf record -e ${perf_event} numactl --membind=${numa_node} ./membench -c -g 2>/dev/null)" | tee -a ${log_file}
echo "perf report --header | egrep Event | sed 's/^.*: //'" | tee -a ${log_file}
rm perf.data
echo -n "${run_n},${node_type},seq_prefetch,$(perf record -e ${perf_event} numactl --membind=${numa_node} ./membench -c -s -p 2>/dev/null)" | tee -a ${log_file}
echo "perf report --header | egrep Event | sed 's/^.*: //'" | tee -a ${log_file}
rm perf.data
echo -n "${run_n},${node_type},rnd_prefetch,$(perf record -e ${perf_event} numactl --membind=${numa_node} ./membench -c -r -p 2>/dev/null)" | tee -a ${log_file}
echo "perf report --header | egrep Event | sed 's/^.*: //'" | tee -a ${log_file}
rm perf.data
echo -n "${run_n},${node_type},pgn_prefetch,$(perf record -e ${perf_event} numactl --membind=${numa_node} ./membench -c -g -p 2>/dev/null)" | tee -a ${log_file}
echo "perf report --header | egrep Event | sed 's/^.*: //'" | tee -a ${log_file}
rm perf.data

#echo -n "${run_n},${node_type},seq,$(perf record -e cache-misses numactl --membind=${numa_node} ./membench -c -s 2>/dev/null)" | tee -a ${log_file}
#echo "perf report --header | egrep Event | sed 's/^.*: //'" | tee -a ${log_file}
#rm perf.data
#echo -n "${run_n},${node_type},rnd,$(perf record -e cache-misses numactl --membind=${numa_node} ./membench -c -r 2>/dev/null)" | tee -a ${log_file}
#echo "perf report --header | egrep Event | sed 's/^.*: //'" | tee -a ${log_file}
#rm perf.data
#echo -n "${run_n},${node_type},pgn,$(perf record -e cache-misses numactl --membind=${numa_node} ./membench -c -g 2>/dev/null)" | tee -a ${log_file}
#echo "perf report --header | egrep Event | sed 's/^.*: //'" | tee -a ${log_file}
#rm perf.data
#echo -n "${run_n},${node_type},seq_prefetch,$(perf record -e cache-misses numactl --membind=${numa_node} ./membench -c -s -p 2>/dev/null)" | tee -a ${log_file}
#echo "perf report --header | egrep Event | sed 's/^.*: //'" | tee -a ${log_file}
#rm perf.data
#echo -n "${run_n},${node_type},rnd_prefetch,$(perf record -e cache-misses numactl --membind=${numa_node} ./membench -c -r -p 2>/dev/null)" | tee -a ${log_file}
#echo "perf report --header | egrep Event | sed 's/^.*: //'" | tee -a ${log_file}
#rm perf.data
#echo -n "${run_n},${node_type},pgn_prefetch,$(perf record -e cache-misses numactl --membind=${numa_node} ./membench -c -g -p 2>/dev/null)" | tee -a ${log_file}
#echo "perf report --header | egrep Event | sed 's/^.*: //'" | tee -a ${log_file}
#rm perf.data
