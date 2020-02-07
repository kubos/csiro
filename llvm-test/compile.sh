#!/bin/sh

export PATH=$PATH:/home/vagrant/armv7m-m3-uclibc-2018/bin
BOM=/vagrant/linux-cortexm-1.14.3

rm clang-main

clang-8 -target thumbv7m-unknown-linux-uclibc \
    --sysroot=/home/vagrant/armv7m-m3-uclibc-2018 \
    -I /home/vagrant/armv7m-m3-uclibc-2018/arm-buildroot-uclinux-uclibcgnueabi/sysroot/usr/include/ \
    -c main.c -o clang-main -v


/home/vagrant/armv7m-m3-uclibc-2018/bin/arm-buildroot-uclinux-uclibcgnueabi-elf2flt -o claing-main-bflt clang-main -a -r