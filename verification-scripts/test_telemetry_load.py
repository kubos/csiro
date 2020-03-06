#!/usr/bin/env python3

# Copyright 2020 Kubos Corporation
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

import app_api
import pytest
from pytest_steps import depends_on
from pytest_steps import test_steps
import time
import random
import json
import string

"""
Integration test for exercising the scheduler and app service in tandem.
It should exercise the path of:
- Transferring & installing an app
"""

SERVICE = "telemetry-service"


def step_query(service_api):
    resp = service_api.query(
        service = SERVICE,
        query = ''' {
            telemetry(subsystem: "test_system", limit: 50) {
                value
            }
        }'''
    )


def step_insert_ten(service_api):
    for t in range(1, 10):
        # Perform Insert
        query = '''
            mutation {
                insert(timestamp: %f,
                        value: "%s",
                        subsystem: "test_system",
                        parameter: "test_param") {
                    success
                }
            }
            ''' % (random.randint(10000, 100000), str(random.randint(100, 1000)))
        resp = service_api.query(
            service = SERVICE,
            query = query
        )
        assert(resp["insert"]["success"] == True)

def step_insert_fifty(service_api):
    for t in range(1, 20):
        # Perform Insert
        query = '''
            mutation {
                insert(timestamp: %f,
                        value: "%s",
                        subsystem: "test_system",
                        parameter: "test_param") {
                    success
                }
            }
            ''' % (random.randint(10000, 100000), str(random.randint(100, 1000)))
        resp = service_api.query(
            service = SERVICE,
            query = query
        )
        assert(resp["insert"]["success"] == True)

def gen_parameter():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))

def step_insert_bulk(service_api):
    entries = []
    for t in range(1, 20):
        entry = '''{ subsystem: "test_system", parameter: "%s", value: "%s"}''' % (gen_parameter(), str(random.randint(10_000, 100_000)))
        entries.append(entry)
    entries = ",".join(entries)
    
    query = '''
            mutation {
                insertBulk(
                    entries: [%s]
                ) {
                    success,
                    errors
                }
            }
    ''' % (entries)
    
    resp = service_api.query(
        service = SERVICE,
        query = query
    )

    assert(True == resp["insertBulk"]["success"])

def step_cleanup(service_api):
    # Cleanup
    service_api.query(
        service = SERVICE,
        query = '''
        mutation {
            delete(subsystem: "test_system") {
                success
            }
        }
        '''
    )

@test_steps(
    step_query,
    step_insert_ten,
    step_query,
    # step_insert_fifty,
    # step_query,
    step_insert_bulk,
    step_query,
    # step_cleanup
)
def test_suite(test_step, service_api):
    random.seed()
    test_step(service_api)

