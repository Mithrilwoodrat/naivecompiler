#!/bin/bash

python compiler.py tests/test3.ns -o test.o
clang tests/test3.c test.o -o test3
./test3
