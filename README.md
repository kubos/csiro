# CSIRO Dev Instructions

## Setting up a dev vm (from scratch)

### Start with KubOS SDK

    vagrant init kubos/kubos-dev

*At this point I would modify the VM in VirtualBox and give it at 
least 8gb of ram and 2-4 cores to speed the compilation process.*

    vagrant up

### Setup VM innards

    vagrant ssh

#### Installing Rust tools

    rustup default nightly-2020-01-28
    cargo install xargo
    rustup component add rust-src

## Once the VM is setup (or if using pre-setup VM)

The following should all be done on the host machine, inside a folder to be shared with the VM.

### Obtain uClibc toolchain

    wget https://toolchains.bootlin.com/downloads/releases/toolchains/armv7m/tarballs/armv7m--uclibc--stable-2018.11-1.tar.bz2 && tar -xvjf armv7m--uclibc--stable-2018.11-1.tar.bz2 && rm armv7m--uclibc--stable-2018.11-1.tar.bz2

### Obtain patched dependencies

A git repo is already setup with git submodules pointing to the patched dependency
repos. 

    git clone https://github.com/kubos/csiro
    cd csiro

*Note: These commands might take some time to run*


    git submodule init
    git submodule update
    cd dependencies/rust
    git submodule init
    git submodule update
    cd ../../..

### Setup new project

A template project is provided in the `project-template` folder.
This template is already setup with the necessary configuration files.
These files assume that the toolchain and `csiro` repo exist in a shared 
folder mounted at `/vagrant` in the VM.

    cd /vagrant
    cp -a /vagrant/csiro/project-template new-project
    cd new-project

This project is setup as a [Cargo workspace](https://doc.rust-lang.org/book/ch14-03-cargo-workspaces.html). This is done to simplify the configuration,
as all the cross-compiling config only needs to exist once in the root of the workspace.

Actual library or binary projects are created inside of the workspace and added
to the `members` variable in the `Cargo.toml`.

### Building projects

Building projects should be done inside of the VM, so you may need to run `vagrant ssh`
or jump in via your virtual machine manager's gui.

The `env.sh` script needs to be sourced to setup necessary environment variables:

    source env.sh

All projects in the workspace can be built with this command:

    RUST_TARGET_PATH=`pwd` xargo build --target thumbv7m-unknown-linux-uclibc

Individual projects can be built with this command:

    RUST_TARGET_PATH=`pwd` xargo build --target thumbv7m-unknown-linux-uclibc --package project-name

All build artifacts will be found in the folder `target/thumbv7m-unknown-linux-uclibc/(release|debug)/` at the root of the workspace.