#!/usr/bin/env python3

# Copyright 20120 Kubos Corporation
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

import app_api
import pytest

"""
Integration test for exercising the app service.
"""

SERVICE = "app-service"

@pytest.fixture
def service_api():
    service_api = app_api.Services("config.toml")
    yield service_api

def test_ping(service_api):
    service_api.query(
        service = SERVICE,
        query = "{ ping }"
    )

def test_app_list(service_api):
    service_api.query(
        service = SERVICE,
        query = '''
        {
            registeredApps {
                active,
                app {
                    name,
                    version,
                    author
                }
            },
            appStatus {
                name,
                version,
                startTime,
                running
            }
        }
        '''
    )