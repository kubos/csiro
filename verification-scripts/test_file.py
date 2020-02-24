#!/usr/bin/env python3

# Copyright 20120 Kubos Corporation
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

import app_api
import pytest
import subprocess

"""
Integration test for exercising the file service.
"""

SERVICE = "file-service"

def file_command(cmd):
    completed = subprocess.run(
        ["kubos-file-client", "-r", "192.168.0.2", cmd],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )
    return str(completed.stdout)

def test_cleanup():
    assert("Operation successful" in file_command("cleanup"))
