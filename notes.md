# Notes

## Version 0
> - `prefetch` data from next iteration;
> - Multiple cacheline accesses;
> - No waitloop.

Observations:
- `prefetch` reduces the cache misses except for sequencial access in PMEM;
- `prefetch` increases the throughput except for sequencial accesses both in PMEM and DRAM;
- The differences in cache misses are less noticeable in PMEM;
- Cache misses are less in PMEM than in DRAM (why?).

```
node_type   access_type  throughput    cache_misses
0       dram           pgn  7392.00000 138053124.00000
1       dram  pgn_prefetch 14966.00000     37355.66667
2       dram           rnd  7638.66667 136599476.33333
3       dram  rnd_prefetch 13291.33333      1807.33333
4       dram           seq 56443.66667     90316.66667
5       dram  seq_prefetch 31897.66667       288.00000
6       pmem           pgn  2079.33333      5766.33333
7       pmem  pgn_prefetch  4614.00000      2974.33333
8       pmem           rnd  2243.33333      5493.00000
9       pmem  rnd_prefetch  4389.33333      3383.66667
10      pmem           seq 55907.66667       279.33333
11      pmem  seq_prefetch 31387.00000       282.33333
```

## Version 1
> - `prefetch` data from next iteration;
> - **Single** cacheline accesses;
> - No waitloop.

Observations:
- `prefetch` reduces the cache misses except for sequencial access in PMEM;
- `prefetch` increases the throughput except for sequencial accesses **only in DRAM**;
- The differences in cache misses are less noticeable in PMEM;
- Cache misses are less in PMEM than in DRAM (why?).

```
node_type   access_type  throughput   cache_misses
0       dram           pgn 35718.00000 98295847.33333
1       dram  pgn_prefetch 41770.66667    80822.33333
2       dram           rnd 27329.66667 97848190.66667
3       dram  rnd_prefetch 32154.33333   213790.00000
4       dram           seq 97312.00000   247549.00000
5       dram  seq_prefetch 94407.66667    42421.33333
6       pmem           pgn  7746.00000     1517.00000
7       pmem  pgn_prefetch  9586.66667     1345.66667
8       pmem           rnd  5913.00000     1988.00000
9       pmem  rnd_prefetch  7566.66667     1310.00000
10      pmem           seq 39733.66667      664.33333
11      pmem  seq_prefetch 40238.66667      898.66667
```

## Version 2
> - `prefetch` data from **current** iteration;
> - **Single** cacheline accesses;
> - With **waitloop** (avoiding compiler optimizations).

```
node_type   access_type  throughput   cache_misses
0       dram           pgn 31172.33333 98319847.33333
1       dram  pgn_prefetch   764.00000  5570311.33333
2       dram           rnd 23147.33333 97840706.00000
3       dram  rnd_prefetch   765.00000     4806.33333
4       dram           seq 97065.66667   254455.66667
5       dram  seq_prefetch   768.00000     2247.00000
6       pmem           pgn  8491.33333     1753.33333
7       pmem  pgn_prefetch   762.50000     1397.00000
8       pmem           rnd  6403.66667     1469.00000
9       pmem  rnd_prefetch   765.33333     1831.33333
10      pmem           seq 40437.66667      592.00000
11      pmem  seq_prefetch   767.66667     2465.33333
```