# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.24

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/jpantao/git/membench

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/jpantao/git/membench

# Include any dependencies generated for this target.
include CMakeFiles/membench.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/membench.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/membench.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/membench.dir/flags.make

CMakeFiles/membench.dir/membench.c.o: CMakeFiles/membench.dir/flags.make
CMakeFiles/membench.dir/membench.c.o: membench.c
CMakeFiles/membench.dir/membench.c.o: CMakeFiles/membench.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/jpantao/git/membench/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object CMakeFiles/membench.dir/membench.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/membench.dir/membench.c.o -MF CMakeFiles/membench.dir/membench.c.o.d -o CMakeFiles/membench.dir/membench.c.o -c /home/jpantao/git/membench/membench.c

CMakeFiles/membench.dir/membench.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/membench.dir/membench.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/jpantao/git/membench/membench.c > CMakeFiles/membench.dir/membench.c.i

CMakeFiles/membench.dir/membench.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/membench.dir/membench.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/jpantao/git/membench/membench.c -o CMakeFiles/membench.dir/membench.c.s

# Object files for target membench
membench_OBJECTS = \
"CMakeFiles/membench.dir/membench.c.o"

# External object files for target membench
membench_EXTERNAL_OBJECTS =

membench: CMakeFiles/membench.dir/membench.c.o
membench: CMakeFiles/membench.dir/build.make
membench: CMakeFiles/membench.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/jpantao/git/membench/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C executable membench"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/membench.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/membench.dir/build: membench
.PHONY : CMakeFiles/membench.dir/build

CMakeFiles/membench.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/membench.dir/cmake_clean.cmake
.PHONY : CMakeFiles/membench.dir/clean

CMakeFiles/membench.dir/depend:
	cd /home/jpantao/git/membench && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/jpantao/git/membench /home/jpantao/git/membench /home/jpantao/git/membench /home/jpantao/git/membench /home/jpantao/git/membench/CMakeFiles/membench.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/membench.dir/depend

