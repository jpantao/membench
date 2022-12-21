#!/bin/bash

cd "$(pwd)" || exit 1

cmake -B build
make clean --directory build
make --directory build

./build/membench