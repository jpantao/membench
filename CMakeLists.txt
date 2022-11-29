cmake_minimum_required(VERSION 3.18)
project (membench C)
set(CMAKE_C_STANDARD 99)

add_executable(membench membench.c)
add_executable(membench_base membench_base.c)
add_executable(membench_data_init membench_data_init.c)
add_executable(membench_pregen_init membench_pregen_init.c)
#target_compile_options(membench PRIVATE -g)
#target_compile_options(membench_base PRIVATE -g)
#target_compile_options(membench_data_init PRIVATE -g)
#target_compile_options(membench_pregen_init.c PRIVATE -g)

add_executable(simplebench simplebench.c)
