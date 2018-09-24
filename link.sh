#!/bin/bash
if [[ "$OSTYPE" == "linux-gnu" ]]; then
     ld -o $2 -dynamic-linker /lib64/ld-linux-x86-64.so.2 /usr/lib/x86_64-linux-gnu/crt1.o /usr/lib/x86_64-linux-gnu/crti.o -lc $1 /usr/lib/x86_64-linux-gnu/crtn.o
elif [[ "$OSTYPE" == "darwin"* ]]; then
    ld -macosx_version_min 10.1 -o $2  /usr/lib/libSystem.dylib /usr/lib/crt1.o $1
else
    echo "unknow platform"
fi

