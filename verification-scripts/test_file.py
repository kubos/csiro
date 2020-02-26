#!/usr/bin/env python3

# Copyright 2020 Kubos Corporation
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

import app_api
import pytest
import subprocess
import filecmp
import tempfile
"""
Integration test for exercising the file service.
"""

SERVICE = "file-service"

def test_cleanup(file_command):
    assert("Operation successful" in file_command(["cleanup"]))

def test_upload_download(file_command, shell_command):
    with tempfile.NamedTemporaryFile() as upload_file:
        upload_file.write(b"Hello Test")
        upload_file.flush()
        assert("Operation successful" in file_command(["upload", upload_file.name, "/test.txt"]))
        with tempfile.NamedTemporaryFile() as download_file:
            assert("Operation successful" in file_command(["download", "/test.txt", download_file.name]))
            assert(filecmp.cmp(upload_file.name, download_file.name))
    
    shell_command(["run", "-c", "rm /test.txt"])