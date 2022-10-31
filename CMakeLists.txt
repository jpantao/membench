cmake_minimum_required(VERSION 3.18)
project (membench C)

set(CMAKE_C_STANDARD 99)

add_executable(membench membench.c)
# target_link_libraries(membench numa)
# target_compile_options(membench PRIVATE -g -pthread)

add_executable(simplebench simplebench.c)