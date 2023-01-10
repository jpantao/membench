cmake_minimum_required(VERSION 3.18)
project (membench C)

set(CMAKE_C_STANDARD 99)
#set(CMAKE_EXE_LINKER_FLAGS "-static")

add_compile_options(-Wall -Wextra -Wpedantic -g)
add_executable(membench membench.c)
add_executable(membench_base membench_base.c)
add_executable(membench_data_init membench_data_init.c)
add_executable(membench_pregen_init membench_pregen_init.c)
