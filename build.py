#!/usr/bin/env python3

import os
import shutil
import difflib
import subprocess
import sys
import contextlib

@contextlib.contextmanager
def pushd(new_dir):
    previous_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(previous_dir)

class StackState:
        BATCH_ONLY = 0
        SH_ONLY = 1
        IF_STATEMENT = 2

        def __init__(self, const, indent):
                self.const = const
                self.indent = indent

stack = []

def get_filter_state():
        for i in stack:
                if (i.const == StackState.BATCH_ONLY or i.const == StackState.SH_ONLY): return i

def silent_system_stdout(command):
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return p.stdout.read()

def silent_system_call(command):
        p = subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        return p.returncode

def system_stdout(command):
        p = subprocess.Popen(command, shell=True)
        return p.returncode

def which(arg):
        return shutil.which(arg)

def exists(arg):
        return os.path.exists(arg)
        
def rd(arg):
        try:
                shutil.rmtree(arg)
                return 1
        except OSError as e:
                print(e)
                return 0

def mkdir(arg):
        return os.mkdir(arg)

def arg(i):
        i += 1 # compensate for this scripts args
        if len(sys.argv) > i:
            return sys.argv[i]

def get_line_indent(line):
        for i in range(len(line)):
                if line[i] not in (" ", "\t"):
                        return i // 4 # python convention is 4 spaces?

preprocessed_code = []

with open(sys.argv[1], "r") as f:
        for line in f:
                command = line.strip()
                if command == "bat {":
                        stack.append(StackState(StackState.BATCH_ONLY, get_line_indent(line)))
                elif command == "sh {":
                        stack.append(StackState(StackState.SH_ONLY, get_line_indent(line)))
                elif command == "}":
                        if (stack):
                                stack.pop()
                        else:
                                print("Missing block starting statement '{'!")
                                break
                else:
                        filter_state = get_filter_state()
                        if os.getenv("SHELL") == "/bin/zsh" and filter_state and filter_state.const == StackState.SH_ONLY:
                                left_trail = "    " * filter_state.indent
                                preprocessed_code.append(f"{left_trail}error_code = os.system('{command}')\n")
                        elif not filter_state or filter_state and filter_state.const not in (StackState.SH_ONLY, StackState.BATCH_ONLY):
                                preprocessed_code.append(line)

        code = "".join(preprocessed_code)
        exec(code)

