# membench

Membench is a simple benchmark for measuring the speed of memory accesses. It allows sequential (`-s`) and random (`-r`
or`-g`) accesses to memory. With the random access pattern, the memory address to be access can be pre-generated (`-g`)
or generated at access time (`-r`). We combine `membench` with `numactl` and `perf` isolating the benchmark to specific
CPU and NUMA nodes and measure other events, such as `cache-misses`. Additionally `membench` allows software prefetching
(`-p`) before each access allowing to measure its impact.

Membench is split in 4 phases:

- **Phase 1**: This phase consists only in argument parsing and initialization of auxiliary variables;
- **Phase 2**: Data array allocation and initialization;
- **Phase 3**: Array with pre-generated random addresses allocation and initialization;
- **Phase 4**: Main loop with data accesses.

#### Phase 2

The benchmark starts by allocating 1GB of memory to the `data` array which is then initialized with random values.

```c
// Data initialization
uint64_t *data = malloc(data_size);
for (register int i = 0; i < data_len; i++) {
data[i] = gen_address_CL64(&seed, data_len);
}
```

Note that the type of the `data` array is `uint64_t` meaning that each cell comprises 8 Bytes, and that 8 cells equate a
cache line of 64 Bytes. The `gen_address_CL64` function here is used to generate random addresses (i.e., array
positions).

#### Phase 3

The `pgn_addr` array is allocated and initialized with random addresses for each future access. The `pgn_addr` array is
used to store the addresses to be used by the benchmark in the pre-generates random access pattern.

```c
// Pregen array initialization
int *pgn_addr = malloc(n_operations * sizeof(int));
for (register int i = 0; i < n_operations; i++) {
pgn_addr[i] = gen_address_CL64(&seed, data_len);
}
```

Here, the `gen_address_CL64` function is used to generate random addresses ensuring that the generated addresses are
aligned to cache lines, i.e., that the addresses are multiples of 8.
`n_operations` represents the number of accesses to be performed by the benchmark.

#### Phase 4

This consists in the main loop with the memory accesses. The loop is repeated `N_ITERATIONS` times.

```c
// Main loop
gettimeofday(&tstart, NULL);
for (register int i = 0; i < n_operations; i++) {
    if (op_seq)
        offset = (offset + cache_line_size) % data_len;
    else if (op_rand)
        offset = gen_address_CL64(&seed, data_len);
    else if (op_pregen)
        offset = pgn_addr[i];
    
    if (op_prefetch)
        __builtin_prefetch(data + offset, 0, 0);
    
    gettimeofday(&spinloop_tstart, NULL);
    spinloop(spinloop_iterations);
    gettimeofday(&spinloop_tend, NULL);
    spinloop_duration += time_diff(&spinloop_tstart, &spinloop_tend);
    
    access_memory(data + offset);
}
gettimeofday(&tend, NULL);
```

Before each access, the `offset` variable is updated with the address to be accessed. The `offset` variable is used to
index the `data` array and is updated according to the access pattern selected by the user.

If the `-p` option is used, the `__builtin_prefetch` function is used to prefetch the data to be accessed
to processor cache. Additionally, and to ensure that the effects of prefetch take place, a spinloop is executed right
after the prefetch. The spinloop is executed `spinloop_iterations` times (which is configurable through a command line
argument).

We calculate the time spent in the main loop and the spinloop separately. In the end, the output of the benchmark is
the throughput (op/ms) measured as `n_operations / mainloop_duration - spinloop_duration`.

## Evaluation

TODO

## Usage

To compile the benchmark, run:

```
cmake -B build
make --directory build
```

The benchmark can be run with:

```
Usage: ./membench [OPTION]...
Benchmark different kinds of memory accesses.

Access types:
  -s            sequential memory access
  -r            random memory access (generate a random address at 'access time')
  -g            random memory access (accesss random pre-generated addresses)
  
Note: only one access type can be selected at a time. If none is selected, the default is sequential access. 

Processor cache prefetch options:
  -p            prefetch data to processor cache before each access (default=do not use prefetch)
  -w <it>       number of iterations for the spinloop after each prefetch (default=0)

Output control:
  -c            output in csv format (throughput)
```

#### Example

This benchmark is used to measure the impact of prefetching on the throughput of random memory accesses. In combination
with `numactl` and `perf`, we can isolate the benchmark to a specific CPU and NUMA node and measure other hardware 
events such as cache misses. 

To extract the number of cache misses in the last level cache (LLC) and the throughput of the benchmark in memory node 0
and CPU node 0 with prefetching enabled in sequential mode and 1000 spinloop iterations, run:


``` 
numactl --membind=0 --cpubind=0 perf stat -e cache-misses ./build/membench -s -p -w 1000
```

The list of available `perf` events can be found [here](https://perf.wiki.kernel.org/index.php/Tutorial#Available_events).

---

## Acknowledgments

This work was partially funded by the Portuguese FCT-MEC project HiPSTr (High-performance Software Transactions — PTDC/CCI-COM/32456/2017)&LISBOA-01-0145-FEDER-032456).
