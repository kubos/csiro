#!/usr/bin/env python3

# Copyright 20120 Kubos Corporation
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

"""
Verification script for the telemetry service.
"""

import app_api

SERVICE = "telemetry-service"

def test_ping():
    service_api = app_api.Services("config.toml")
    resp = service_api.query(
        service = SERVICE,
        query = "{ ping }"
    )
    assert(resp["ping"] == "pong")

def test_query():
    service_api = app_api.Services("config.toml")
    resp = service_api.query(
        service = SERVICE,
        query = ''' {
            telemetry(subsystem: "test_system") {
                value
            }
        }'''
    )
    assert(resp["telemetry"] == [])

def test_insert():
    service_api = app_api.Services("config.toml")
    
    # Perform Insert
    resp = service_api.query(
        service = SERVICE,
        query = '''
        mutation {
            insert(timestamp: 11111,
                    value: "test_value",
                    subsystem: "test_system",
                    parameter: "test_param") {
                success
            }
        }
        '''
    )
    assert(resp["insert"]["success"] == True)
    
    # Verify Insert
    resp = service_api.query(
        service = SERVICE,
        query = ''' {
            telemetry(subsystem: "test_system") {
                value
            }
        }'''
    )
    assert(resp["telemetry"][0]["value"] == "test_value")

    # Cleanup

    resp = service_api.query(
        service = SERVICE,
        query = '''
            mutation {
                delete(timestampGe: 0) {
                    success
                }
            }
        '''
    )
    assert(resp["delete"]["success"] == True)