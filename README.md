# membench

Membench is a simple benchmark for measuring the speed of memory access. It allows sequential (`-s`) and random (`-r` or
`-g`) accesses to memory. With the random access pattern, the memory address to be access can be pre-generated (`-g`) or 
generated at access time (`-r`). We combine `membench` with `numactl` and `perf` isolating the benchmark to specific
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
for(register int i = 0; i < data_len; i++) {
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
int *pgn_addr = malloc(N_OPERATIONS * sizeof(int));
for (register int i = 0; i < N_OPERATIONS; i++) {
    pgn_addr[i] = gen_address_CL64(&seed, data_len);
}
```

Here, the `gen_address_CL64` function is used to generate random addresses ensuring that the generated addresses are 
aligned to cache lines, i.e., that the addresses are multiples of 8.
`N_OPERATIONS` represents the number of accesses to be performed by the benchmark. 

#### Phase 4

This consists in the main loop with the memory accesses. The loop is repeated `N_ITERATIONS` times. 
```c
// Main loop
gettimeofday(&tstart, NULL);
for (register int i = 0; i < N_OPERATIONS; i++) {
    
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

In

### Usage

```
Usage: ./membench [OPTION]...
Benchmark different kinds of memory accesses.

Access types:
  -s            sequential memory access
  -r            random memory access (generate a random address at 'access time')
  -g            random memory access (accesss random pre-generated addresses)

Processor cache prefetch options:
  -p            prefetch data to processor cache before each access (default=do not use prefetch)
  -w iterations number of iterations for the spinloop after each prefetch (default=0)

Output control:
  -c            output in csv format (throughput,cache_misses)
```


---

[//]: # (### Running on Grid 5000)

[//]: # ()
[//]: # (Pushing the code to the site:)

[//]: # (```)

[//]: # (./scripts/push-code.sh grenoble.g5k)

[//]: # (```)

[//]: # ()
[//]: # (Passive reservation:)

[//]: # (```)

[//]: # (oarsub -t exotic -p "cluster='troll'" -t deploy -l nodes=1,walltime=1 "./scripts/deploy-test.sh <test_name> <n_runs>")

[//]: # (```)
