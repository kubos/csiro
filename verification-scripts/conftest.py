#!/usr/bin/env python3

# Copyright 2020 Kubos Corporation
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

import pytest
import subprocess
import app_api

@pytest.fixture
def service_api():
    service_api = app_api.Services("config.toml")
    yield service_api

@pytest.fixture
def shell_command():
    def stub(args):
        shell_args = ["kubos-shell-client", "-i", "192.168.0.2"]
        shell_args.extend(args)
        completed = subprocess.run(
            shell_args,
            stdout = subprocess.PIPE
        )
        return str(completed.stdout)
    return stub

@pytest.fixture
def file_command():
    def stub(args):
        file_args = ["kubos-file-client", "-r", "192.168.0.2"]
        file_args.extend(args)
        completed = subprocess.run(
            file_args,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )
        return str(completed.stdout)
    return stub