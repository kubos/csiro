#!/bin/sh

export PATH=$PATH:/home/vagrant/arm-2010q1/bin

clang-8 -target thumbv7m-unknown-linux-uclibc \
    --sysroot=/home/vagrant/arm-2010q1 \
    -I/home/vagrant/arm-2010q1/arm-uclinuxeabi/libc/usr/include/ \
    -c main.c -o main