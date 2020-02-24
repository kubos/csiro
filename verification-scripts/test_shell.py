#!/usr/bin/env python3

# Copyright 20120 Kubos Corporation
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

import app_api
import pytest
import subprocess

"""
Integration test for exercising the shell service.
"""

SERVICE = "shell-service"

def shell_command(cmd):
    completed = subprocess.run(
        ["kubos-shell-client", "-i", "192.168.0.2", cmd],
        stdout = subprocess.PIPE
    )
    return str(completed.stdout)

def test_list():
    assert("No active sessions" in shell_command("list"))
