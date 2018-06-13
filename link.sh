#!/bin/bash
ld -o $2 -dynamic-linker /lib64/ld-linux-x86-64.so.2 /usr/lib/x86_64-linux-gnu/crt1.o /usr/lib/x86_64-linux-gnu/crti.o -lc $1 /usr/lib/x86_64-linux-gnu/crtn.o