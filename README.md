# Mantle
Automated build tool

### Features: 
1. simple and compact
2. incremental builds
3. supports multiple main functions
4. supports cross-compilation
5. target multiple platforms simultaneously
6. quickly change configuration to suite your project's needs

Mantle will automatically find, build, and link all source files under the src directory.	
This builder is incremental, and will only rebuild source files that have changed	since the last build. 
The header files are also recursively checked for changes. 

Mantle is compatible with multiple entry points (main functions). 
It will quickly scan all source files for these entry points, and then produce a binary for each. 
The binary is named after the source file with the entry point.

Mantle is configured via its two configuration files: project.config and toolchain.config. 
These config files are assumed to be in the CWD when executing Mantle.

