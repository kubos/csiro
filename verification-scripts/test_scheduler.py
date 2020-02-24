#!/usr/bin/env python3

# Copyright 20120 Kubos Corporation
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

import app_api
import pytest

"""
Integration test for exercising the scheduler service.
"""

SERVICE = "scheduler-service"

@pytest.fixture
def service_api():
    service_api = app_api.Services("config.toml")
    yield service_api

def test_ping(service_api):
    service_api.query(
        service = SERVICE,
        query = "{ ping }"
    )

def test_initial_active_mode(service_api):
    active_mode = service_api.query(
        service = SERVICE,
        query = "{ activeMode { name } }"
    )
    assert(active_mode["activeMode"]["name"] == "safe")