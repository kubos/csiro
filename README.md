# CSIRO Dev Instructions

These instructions detail how to setup a development environment for cross-compiling for the CSIRO board.

## Folder Structure

We're going to establish a standard folder structure to ensure that everything ends up in the correct place.

`$DEV` - This should be a folder on your local dev computer which will contain all development dependencies 
and will be shared with the development VM.

## Setting up a dev vm (from scratch)

Ideally you will already have a VM with the necessary rust components installed. If not then these initial instructions
will guide you through the VM setup process.

### Start with KubOS SDK

We are going to use the [Kubos SDK](https://docs.kubos.com/1.20.0/sdk-docs/sdk-installing.html) as our starting point.
Please take a look at the [SDK instructions](https://docs.kubos.com/1.20.0/sdk-docs/sdk-installing.html) and install
the necessary dependencies like VirtualBox and Vagrant.

    cd $DEV
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

The following should all be done on the host machine, inside the $DEV folder to be shared with the VM.

### Obtain uClibc toolchain

    cd $DEV
    wget https://toolchains.bootlin.com/downloads/releases/toolchains/armv7m/tarballs/armv7m--uclibc--stable-2018.11-1.tar.bz2 && tar -xvjf armv7m--uclibc--stable-2018.11-1.tar.bz2 && rm armv7m--uclibc--stable-2018.11-1.tar.bz2

You should now have the folder `$DEV/armv7m--uclibc--stable-2018.11-1` containing all the toolchain folders/files. 

### Obtain patched dependencies

A git repo is already setup with git submodules pointing to the patched dependency
repos. 

    cd $DEV
    git clone https://github.com/kubos/csiro
    cd csiro

*Note: These commands might take some time to run*


    git submodule init
    git submodule update
    cd dependencies/rust
    git submodule init
    git submodule update
    cd $DEV

Your folder structure should now look like this:

    $DEV                                    - Folder shared with VM
     |-- armv7m--uclibc--stable-2018.11-1   - The GCC cross-compiling toolchain
     |-- csiro                              - Contents of https://github.com/kubos/csiro
          |-- dependencies                  - Patched Rust dependencies
          |-- project-template              - Initial Project Template
          |-- hello-world
          |-- llvm-test

*Note: The hello-world and llvm-test folders are artfiacts of the compiler bring-up process and can be ignored.*

### Setup new project

A template project is provided in the `project-template` folder.
This template is already setup with the necessary configuration files.
These files assume that the toolchain and `csiro` repo exist in a shared 
folder mounted at `/vagrant` in the VM. 

These instructions are assumed to be executed from within the VM, 
so you may need to run `vagrant ssh` or jump in via your virtual machine manager's gui.

    cd /vagrant
    cp -a /vagrant/csiro/project-template /vagrant/new-project
    cd /vagrant/new-project

This project is setup as a [Cargo workspace](https://doc.rust-lang.org/book/ch14-03-cargo-workspaces.html). 
This is done to simplify the configuration, as all the cross-compiling config only needs to exist once in 
the root of the workspace.

Actual library or binary projects are created inside of the workspace and added
to the `members` variable in the `Cargo.toml`.

### Building projects

Building projects should be done inside of the VM, so you may need to run `vagrant ssh`
or jump in via your virtual machine manager's gui.

These instructions are assumed to be executed from within the root project folder:

    cd /vagrant/new-project

The `env.sh` script needs to be sourced to setup necessary environment variables:

    source env.sh

All packages (binary or library) in the workspace can be built with this command:

    RUST_TARGET_PATH=`pwd` xargo build --target thumbv7m-unknown-linux-uclibc

Individual packages (binary or library) can be built with this command:

    RUST_TARGET_PATH=`pwd` xargo build --target thumbv7m-unknown-linux-uclibc --package package-name

All build artifacts will be found in the folder `target/thumbv7m-unknown-linux-uclibc/(release|debug)/` at the root of the workspace.