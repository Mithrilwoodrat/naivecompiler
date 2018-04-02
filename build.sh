#!/bin/bash

cd backend
mkdir build
cd build
cmake ..
make
cp ./libNaiveScript.so ../../
