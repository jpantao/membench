# membench

> Benchmark memory access.

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


### Running on Grid 5000

Pushing the code to the site:
```
./scripts/push-code.sh grenoble.g5k
```

Passive reservation:
```
oarsub -t exotic -p "cluster='troll'" -t deploy -l nodes=1,walltime=1 "./scripts/deploy-test.sh <test_name> <n_runs>"
```
