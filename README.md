# Mantle
Automated C++ build tool

### Getting Started
1. Clone Mantle into the root of your project directory

        git https://github.com/jpxor/Mantle.git build

2. Update the project configuration

    a. Select one or more toolchains and target platforms

        // Building with gcc for Linux: 
            "BUILD_TARGET":{ "gcc": ["linux64"], },

        // Building with clang and qcc for Linux, Windows, and QNX: 
            "BUILD_TARGET":{ "clang": ["linux64", "win64"], "qcc": ["qnx-x86-64", "qnx-aarch64le"] },

    b. Add your project's required include directories, and per target libraries and build flags.
    
        "INCLUDE_DIR": [ "../src/include" ], 
        "TARGETS": { "linux64":{ "LIBS": ["GL"], "CFLAGS":"-Wall" } } 

3. Build your project from the build directory

        cd build
        mantle.py build

### Features: 
- simple and compact
- incremental builds
- supports multiple main functions
- supports cross-compilation
- target multiple platforms simultaneously
- quickly change configuration to suite your project's needs

Mantle will automatically find, build, and link all source files under the src directory.	
This builder is incremental, and will only rebuild source files that have changed since the last build. 
The header files are also recursively checked for changes. 

Mantle is compatible with multiple entry points (main functions). 
It will quickly scan all source files for these entry points, and then produce a binary for each. 
The binary is named after the source file with the entry point.

Mantle is configured via its two configuration files: project.config and toolchain.config. 
These files are assumed to be in the CWD when executing Mantle.

### Project Configuration
