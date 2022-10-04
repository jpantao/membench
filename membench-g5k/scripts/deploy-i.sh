#!/bin/bash

oarsub -t exotic -p "cluster='troll'" -t deploy -l nodes=1 -I
./scripts/deploy.sh 