#!/bin/sh

export PATH=$PATH:/home/vagrant/arm-2010q1/bin
BOM=/vagrant/linux-cortexm-1.14.3

rm arm-main

arm-uclinuxeabi-gcc  \
    -mthumb  -mcpu=cortex-m3 \
    -fPIC \
    -pthread \
    -I $BOM/A2F/root/usr/include \
    -L $BOM/A2F/root/usr/lib \
    main.c -o arm-main 