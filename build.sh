#!/bin/bash

cd backend
cmake .
make
cp build/libNaiveScript.so ../
