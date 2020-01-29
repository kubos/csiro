use std::io;
use std::io::prelude::*;
use std::fs::File;
use std::io::BufWriter;

fn calc_return() -> i32 {
    let num = 10;
    let second = 6;
    num + second
}

fn test_vars() {
    let num = 10;
    let vec = vec![1,2,3,4];
    let name = "Ryan";
    let alive = true;
}

pub fn main() {
    test_vars();
    let f = File::create("hi.txt").unwrap();
    {
        let mut writer = BufWriter::new(f);
        writer.write("Hello".as_bytes()).unwrap();
    }
    println!("Hello Rusty Cortex-M3");
    std::process::exit(calc_return());
}