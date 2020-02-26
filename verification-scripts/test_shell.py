#!/usr/bin/env python3

# Copyright 2020 Kubos Corporation
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

import app_api
import pytest
import subprocess

"""
Integration test for exercising the shell service.
"""

SERVICE = "shell-service"


def test_list(shell_command):
    assert("No active sessions" in shell_command(["list"]))

def test_cmd(shell_command):
    assert("can't execute" not in shell_command(["run", "-c", "ls /"]))
