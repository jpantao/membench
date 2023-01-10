cmake_minimum_required(VERSION 3.18)
project (membench C)

set(CMAKE_C_STANDARD 99)
#set(CMAKE_EXE_LINKER_FLAGS "-static")
add_compile_options(-Wall -Wextra -Wpedantic -g)

add_executable(membench membench.c)

