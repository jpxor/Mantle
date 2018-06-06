# Mantle 
Build automation for your C++ projects
#### Get your new projects building immediately. Skip the setup and maintenance of recipes and makefiles. Later, extend functionality with a few lines of python. 
- incremental builds
- supports multiple main functions
- simple cross-compilation
- and can target multiple platforms simultaneously

Mantle will automatically find, build, and link all source files under the src directory.	
This builder is incremental, and will only rebuild source files that have changed since the last build. 
The header files are also recursively checked for changes. 

Mantle is compatible with multiple entry points (main functions). 
It will quickly scan all source files for these entry points, and then produce a binary for each. 
The binary is named after the source file with the entry point.

Mantle is configured via its two configuration files: project.config and toolchain.config. 
These files are assumed to be in the CWD when executing Mantle.

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


### Is Mantle Right For You? 
Mantle is currently intended for small to medium projects that don't require a complex dependancy graph. Future updates will have options for scaling to larger projects and build orders. 

### Project Configuration
The configuration files use JSON format to specify key-value pairs. Smart defaults are selected to get building as soon as possible.
- SRC_PATH: this directory is recursively searched to find all source files.

      "SRC_PATH": "../src",

- BIN_PATH: binaries are installed into this path. 

      "BIN_PATH": "../bin",
      
- SRC_EXT: specifies extension used to identify source files. 

      "SRC_EXT": [".c", ".cpp", ".c++"],
      
- ENTRY_POINT: specifies the function named used as an entry point. 

      "ENTRY_POINT": "main", 

- CLEAN_EXT: specifies extensions of files to be deleted during cleaning.

      "CLEAN_EXT": [".o"],

- BUILD_TARGET: specifies build targets and which toolchain to use.

      "BUILD_TARGET":{
          "clang": ["win64", "linux64"],
          "qcc": ["qnx-x86-64"],
      },	

- TARGETS: specifies which targets are explicitly supported by your projcet, and lists target dependant configurations.
  - LIBS: list of libraries
  - CFLAGS: compiler flags
  - LDFLAGS: linker flags (may need to use -Wl option for some toolchains)

        "TARGETS": {
            "linux64":{
                "LIBS": ["GL"],
                "CFLAGS":"-Wall",
                "LDFLAGS":"-Wl"
            },
        },

### Toolchain Configuration
This file describes the build command and link command for each toolchain. You should't have to change anything in this file unless you are adding a new toolchain or target will specific needs. Here are two example toolchain configurations: 

- clang on Windows and Linux

      "clang":{
          "win64":{
              "BIN_EXTENTION":".exe",
              "INC_PREFIX":"-I",
              "LIB_PREFIX":"-l", 
              "BUILD_CMD":"clang++ -c [CFLAGS] [INCLUDE_DIRS] -o [OBJ_PATH] [SRC_FILE]", 
              "LINK_CMD": "clang++ -o [BIN] [LDFLAGS] [OBJ_FILES] [LIBS]"
          },
          "linux64":{
              "BIN_EXTENTION":"",
              "INC_PREFIX":"-I",
              "LIB_PREFIX":"-l", 
              "BUILD_CMD":"clang++ -c [CFLAGS] [INCLUDE_DIRS] -o [OBJ_PATH] [SRC_FILE]", 
              "LINK_CMD": "clang++ -o [BIN] [LDFLAGS] [OBJ_FILES] [LIBS]"
          }
      },
      
- qcc targeting QNX on x86_64 and aarch64 (cross-compiling from Linux or Windows host)

      "qcc":{
          "qnx-x86-64":{
              "BIN_EXTENTION":"",
              "INC_PREFIX":"-I",
              "LIB_PREFIX":"-l", 
              "BUILD_CMD":"qcc -lang-c++ -Vgcc_ntox86_64 -c [CFLAGS] [INCLUDE_DIRS] -o [OBJ_PATH] [SRC_FILE]",
              "LINK_CMD": "qcc -lang-c++ -Vgcc_ntox86_64 -o [BIN] [LDFLAGS] [OBJ_FILES] [LIBS]"
          }, 
          "qnx-aarch64le":{
              "BIN_EXTENTION":"",
              "INC_PREFIX":"-I",
              "LIB_PREFIX":"-l", 
              "BUILD_CMD":"qcc -lang-c++ -Vgcc_ntoaarch64le -c [CFLAGS] [INCLUDE_DIRS] -o [OBJ_PATH] [SRC_FILE]",
              "LINK_CMD": "qcc -lang-c++ -Vgcc_ntoaarch64le -o [BIN] [LDFLAGS] [OBJ_FILES] [LIBS]"
          }
      },
