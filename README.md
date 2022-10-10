# membench

### Running on Grid 5000

Pushing the code to the site:
```
./scripts/push-code.sh grenoble.g5k
```

Passive reservation:
```
oarsub -t exotic -p "cluster='troll'" -t deploy -l nodes=1,walltime=1 "./scripts/deploy-test.sh ../public/kmem_dax_env.dsc bench 1"
```
