Build Instructions
------------------

Extract vendor toolchain to `/path/to/toolchain`.
Clone https://github.com/kubos/rust to `/path/to/rust` and checkout the `thumbv7m-uclibc-port` branch.

Install the rust dependencies::

    rustup default nightly
    cargo install xargo
    rustup component add rust-src

Set the necessary env vars::

    export CC=/path/to/toolchain/bin/arm-uclinuxeabi-gcc
    export CXX=/path/to/toolchain/bin/arm-uclinuxeabi-g++
    export XARGO_RUST_SRC=/path/to/rust/src

Run the `xargo` build command::

    xargo build --target thumbv7m-unknown-linux-uclibc

Sometimes `xargo` won't do a full rebuild when you need it to. Delete the `$HOME/.xargo` folder and it should then do a full rebuild.