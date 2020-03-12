#!/usr/bin/env python3

# Copyright 20120 Kubos Corporation
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

"""
Verification script for the monitor service.
"""

import app_api

SERVICE = "monitor-service"

def test_ping():
    service_api = app_api.Services("config.toml")
    service_api.query(
        service = SERVICE,
        query = "{ ping }"
    )

def test_ps():
    service_api = app_api.Services("config.toml")
    ps_list = service_api.query(
        service = SERVICE,
        query = "{ ps { pid } }",
        timeout = 30
    )
    print(ps_list)

def test_mem_info():
    service_api = app_api.Services("config.toml")
    data = service_api.query(
        service = SERVICE,
        query = "{ memInfo { total } }"
    )
    assert(data['memInfo']['total'])