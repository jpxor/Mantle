#!/usr/bin/env python3

# MIT License
# Copyright (c) 2017 Josh Simonot

"""
	This module will find and build all source files under the src directory
	and then link them, creating binaries in the bin directory.

	This builder is incremental, and will only rebuild source files that have changed
	since the last build. The header files are also recursively checked for changes.

	This builder is compatible with multiple entry points (main functions), and
	will produce one binary per entry point. The binary is named after the source
	file with the entry point.

	project.config and toolchain.config are assumed to be in the cwd.

    Uses:
        python mantle.py
        python mantle.py build
        python mantle.py clean
        python mantle.py clean build
"""

# ignore "C0103:Invalid constant name":
# pylint: disable=invalid-name

import os
import sys
import json
import subprocess


def find_header_path(header_name, include_dirs):
    """ find and return the pathname to filename """
    for include_dir in include_dirs:
        header_path = os.path.join(include_dir, header_name)
        if os.path.isfile(header_path):
            return os.path.abspath(header_path)
    return None



def get_headers(src_path, include_dirs):
    """ list all included headers in src """
    headerlist = []
    with open(src_path, 'r') as srcfile:
        lines = srcfile.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith("#include"):
                headername = line[10:-1].strip()
                headerpath = find_header_path(headername, include_dirs)
                if headerpath is not None:
                    headerlist.append(headerpath)
                    # recurse to check all included files
                    headerlist.extend(get_headers(headerpath, include_dirs))
    return headerlist



def needs_recompile(src_path, obj_path, include_dirs):
    """ determine if src file needs recompile """

    # check if obj file exists
    if not os.path.isfile(obj_path):
        return True

    # check src file modification time
    if os.path.getmtime(src_path) > os.path.getmtime(obj_path):
        return True

    # check header files' modification time
    for header_path in get_headers(src_path, include_dirs):
        header_path = header_path.rstrip()
        if os.path.isfile(header_path):
            if os.path.getmtime(header_path) > os.path.getmtime(obj_path):
                return True

    return False



# load toolchain config,
tconf = {}
with open("toolchain.config", 'r') as conffile:
    tmpconf = json.loads(conffile.read())
    for key, val in tmpconf.items():
        tconf[key] = val



# load project config,
pconf = {}
with open("project.config", 'r') as conffile:
    tmpconf = json.loads(conffile.read())
    for key, val in tmpconf.items():
        pconf[key] = val



#parse command line args
if len(sys.argv) == 1:
    sys.argv.append("build")

# clean deletes all files matching CLEAN_EXT
if "clean" in sys.argv:
    for root, subdirs, files in os.walk(pconf["SRC_PATH"]):
        for file in files:
            name, ext = os.path.splitext(file)
            if ext in pconf["CLEAN_EXT"]:
                path = os.path.join(root, file)
                print("Cleaning:", path)
                os.remove(path)
    if "build" not in sys.argv:
        exit()



# find all source files,
# find all files with an entry point,
src_list = []
src_main = {}
for root, subdirs, files in os.walk(pconf["SRC_PATH"]):
    for file in files:
        name, ext = os.path.splitext(file)
        if ext in pconf["SRC_EXT"]:
            file_path = os.path.join(root, file)
            src_list.append(file_path)
            with open(file_path, 'r') as fd:
                if pconf["ENTRY_POINT"] in fd.read():
                    src_main[file_path] = (root, name)



# build and link for each targeted platform
for toolchain, targets in pconf["BUILD_TARGET"].items():
    for target in targets:
        toolconfig = tconf[toolchain][target]

        INCLUDE_DIRS = ""
        for inc_path in pconf["INCLUDE_DIR"]:
            INCLUDE_DIRS += " " + toolconfig["INC_PREFIX"] + inc_path

        # build all source files and track object files
        obj_files = {}
        for SRC_FILE in src_list:
            basename, ext = os.path.splitext(SRC_FILE)
            OBJ_PATH = basename + "." + target + ".o"
            obj_files[SRC_FILE] = OBJ_PATH

            if needs_recompile(SRC_FILE, OBJ_PATH, pconf["INCLUDE_DIR"]):
                BUILD_CMD = toolconfig["BUILD_CMD"]
                BUILD_CMD = BUILD_CMD.replace("[CFLAGS]", pconf["TARGETS"][target]["CFLAGS"])
                BUILD_CMD = BUILD_CMD.replace("[INCLUDE_DIRS]", INCLUDE_DIRS)
                BUILD_CMD = BUILD_CMD.replace("[OBJ_PATH]", OBJ_PATH)
                BUILD_CMD = BUILD_CMD.replace("[SRC_FILE]", SRC_FILE)

                print("\nBuilding:", SRC_FILE)
                print(BUILD_CMD)
                BUILD_CMD = list(filter(None, BUILD_CMD.split(' ')))
                subprocess.call(BUILD_CMD)

            else:
                print("Nothing to be done for:", SRC_FILE)

        # link all object files into executables
        for entry_src, attr in src_main.items():
            root = attr[0]
            bin_name = attr[1] + toolconfig["BIN_EXTENTION"]

            LIBS = ""
            for lib in pconf["TARGETS"][target]["LIBS"]:
                LIBS += " " + toolconfig["LIB_PREFIX"] + lib

            bin_path = os.path.relpath(root, pconf["SRC_PATH"])
            bin_path = os.path.join(pconf["BIN_PATH"], target, bin_path)
            if not os.path.isdir(bin_path):
                os.makedirs(bin_path)

            BIN = os.path.join(bin_path, bin_name)

            OBJ_FILES = obj_files[entry_src]
            for src, obj in obj_files.items():
                if src not in src_main:
                    OBJ_FILES += " " + obj

            LINK_CMD = toolconfig["LINK_CMD"]
            LINK_CMD = LINK_CMD.replace("[BIN]", BIN)
            LINK_CMD = LINK_CMD.replace("[LDFLAGS]", pconf["TARGETS"][target]["LDFLAGS"])
            LINK_CMD = LINK_CMD.replace("[OBJ_FILES]", OBJ_FILES)
            LINK_CMD = LINK_CMD.replace("[LIBS]", LIBS)

            print("\nLinking:", bin_name)
            print(LINK_CMD)
            LINK_CMD = list(filter(None, LINK_CMD.split(' ')))
            subprocess.call(LINK_CMD)
