# uClinux Dev Instructions

These instructions detail how to setup a development environment for cross-compiling for the uClinux environment.

## Setting up a dev environment (from scratch)

Ideally you will already have an environment (VM or local) with the necessary
rust components installed. If not then these initial instructions will guide you
through the setup process.

### Start with KubOS SDK

We suggest using the Kubos SDK, a Vagrant-based VM, as a starting point.
Please take a look at the
[SDK instructions](https://docs.kubos.com/1.20.0/sdk-docs/sdk-installing.html) 
and install the necessary dependencies like VirtualBox and Vagrant.

Using vagrant, we initialize and enter the VM with the following commands:

    vagrant init kubos/kubos-dev
    vagrant up
    vagrant ssh

### BYOE (Bring Your Own Environment)

You may have your own VM you want to use, or just do everything in your host
environment. If that is the case, then you'll want to have the following
system dependencies installed in your environment of choice:

- git
- curl
- Rust + Cargo (We suggest using [rustup](https://rustup.rs/))
- gcc
- pkg-config
- libssl-dev or openssl-dev

#### VM Modifications

We suggest making the following modifications if using a VM environment:

- Bump available system RAM to at least 8GB
- Bump available processors to 2 or more
- [Setup shared folder](https://docs.kubos.com/1.20.0/sdk-docs/sdk-installing.html#mount-directory)
  for easily file sharing with the host (note: this will not work on Windows hosts)

#### Installing Extra Rust tools

This step is required whether you are starting with the Kubos SDK or your own environment:

    rustup default nightly-2020-01-29
    cargo install xargo
    rustup component add rust-src

#### Installing Bootlin Toolchain

We are going to be using a uClibc toolchain from [Bootlin](https://toolchains.bootlin.com/).
This toolchain just needs to be extracted into an easily accessible location.

    wget https://toolchains.bootlin.com/downloads/releases/toolchains/armv7m/tarballs/armv7m--uclibc--stable-2018.11-1.tar.bz2 \
    && tar -xvjf armv7m--uclibc--stable-2018.11-1.tar.bz2 \
    && rm armv7m--uclibc--stable-2018.11-1.tar.bz2

*Note: If you are on a Windows host and using a VM, then the toolchain cannot be
placed in a shared folder due to symlink issues*

#### Obtain patched dependencies

Part of the special Rust setup is patched versions of certain Rust crates. A git repo
has been setup with git submodules pointing to the patched dependency repos. 

    git clone https://github.com/kubos/uclinux-port
    cd uclinux-port

*Note: These commands might take some time to run.*

    git submodule init
    git submodule update
    cd dependencies/rust
    git submodule init
    git submodule update

*Note: The hello-world and llvm-test folders in the uclinux-port folder are artifacts of 
the compiler bring-up process and can be ignored.*

#### Sqlite Dependency

Certain Kubos packages have a dependency on sqlite. A copy of the cross-compiled
sqlite library is supplied at `uclinux-port/dependencies/libsqlite3.a`. This file will need to
be copied over to `/path/to/armv7m--uclibc--stable-2018.11-1/arm-buildroot-uclinux-uclibcgnueabi/sysroot/usr/lib`
before cross-compiling any projects with a sqlite dependency.

### Setup new project

A template project is provided in the `project-template` folder. This template is 
already setup with the necessary configuration files and just needs to be copied
to a new location.

    cd /path/to/uclinux-port
    cp -a project-template /path/to/new-project
    cd /path/to/new-project

*Note: The new-project folder must exist outside of the uclinux-port repo folder.*

This project is setup as a [Cargo workspace](https://doc.rust-lang.org/book/ch14-03-cargo-workspaces.html). 
This is done to simplify the configuration, as all the cross-compiling config 
only needs to exist once in the root of the workspace.

Actual library or binary projects are created inside of the workspace and added
to the `members` variable in the root `Cargo.toml` file.

#### Project Configuration

The template project comes with the following configuration files. These files currently
assume that the toolchain and `uclinux-port` repo exist inside of the folder `/vagrant`
(the default shared folder of the Kubos SDK). These files will need adjusting if your
toolchain and `uclinux-port/dependencies` folder exist in another location.

- **thumbv7m-unknown-linux-uclibc.json** - 
    A target specification for the Rust cross compiler. This file has one 
    reference to the toolchain which may need to be updated.
- **Cargo.toml** -
    The root workspace configuration file. This file has multiple references to the folders
    under uclinux-port/dependecies which may need to be updated. This file also has a `members`
    variable which must contain references to all projects in the workspace.
- **Xargo.toml** -
    A cross-compiling configuration file. This file has two references to folders under
    uclinux-port/dependecies which may need to be updated.
- **env.sh** -
    A script to set environment variables. This file has references to the toolchain
    and folders under uclinux-port/dependencies which may need to be updated.
- **.cargo/config** -
    A Rust/Cargo configuration file. This file has two references to the toolchain
    which may need to be updated.

The template project also comes with a `hello-world` folder which is just a simple
Rust "Hello World" binary package. 

### Building projects

These instructions are assumed to be executed from within the root project folder:

    cd /path/to/new-project

The `env.sh` script needs to be sourced to setup necessary environment variables:

    source env.sh

All packages (binary or library) in the workspace can be built with this command:

    RUST_TARGET_PATH=`pwd` xargo build --target thumbv7m-unknown-linux-uclibc

Individual packages (binary or library) can be built with this command:

    RUST_TARGET_PATH=`pwd` xargo build --target thumbv7m-unknown-linux-uclibc --package package-name

All build artifacts will be found in the folder `target/thumbv7m-unknown-linux-uclibc/(release|debug)/` at the root of the workspace.
