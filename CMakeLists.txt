cmake_minimum_required(VERSION 3.18)
project (membench C)
set(CMAKE_C_STANDARD 99)

add_compile_options(-Wall -Wextra -Wpedantic -O3)

add_executable(membench_randr membench_randr.c)
add_executable(membench_lehmer membench_lehmer.c)
add_executable(membench_wyhash membench_wyhash.c)

#add_executable(simplebench simplebench.c)
