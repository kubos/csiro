#!/usr/bin/env python3

# Copyright 2020 Kubos Corporation
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

import app_api
import pytest
from pytest_steps import depends_on
from pytest_steps import test_steps
import time

"""
Integration test for exercising the scheduler and app service in tandem.
It should exercise the path of:
- Transferring & installing an app
"""

APP = "app-service"
SCHEDULER = "scheduler-service"

def step_prepare(shell_command, file_command, service_api):
    # Transfer app
    for i in range(1,6):
        shell_command(["run", "-c", "mkdir /mission-app-{}".format(i)])
        assert("Operation successful" in file_command(["upload", "mission-app-{}/manifest.toml".format(i), "/mission-app-{}/manifest.toml".format(i)]))
        assert("Operation successful" in file_command(["upload", "mission-app-{}/test.sh".format(i), "/mission-app-{}/test.sh".format(i)]))
        assert("Operation successful" in file_command(["upload", "mission-app-{}/testTask.json".format(i), "/mission-app-{}/testTask.json".format(i)]))
    

@depends_on(step_prepare)
def step_register(shell_command, file_command, service_api):
    for i in range(1,6):
        resp = service_api.query(
            service = APP,
            query = '''
            mutation {
                register(path: "/mission-app-%d") {
                    success,
                    errors,
                    entry {
                        active,
                        app {
                            name,
                            version
                        }
                    }
                }
            }
            ''' % i
        )
        if True != resp["register"]["success"]:
            print(resp["register"]["errors"])

        assert(True == resp["register"]["success"])

@depends_on(step_register)
def step_create_mode(shell_command, file_command, service_api):
    # Create test mode
    resp = service_api.query(
        service = SCHEDULER,
        query = '''
            mutation {
                createMode(name: "testMode") {
                    success
                }
            }
        '''
    )
    assert(True == resp["createMode"]["success"])

@depends_on(step_create_mode)
def step_activate_mode(shell_command, file_command, service_api):
    # Activate test mode
    resp = service_api.query(
        service = SCHEDULER,
        query = '''
            mutation {
                activateMode(name: "testMode") {
                    success
                }
            }
        '''
    )
    assert(True == resp["activateMode"]["success"])

@depends_on(step_activate_mode)
def step_schedule_app(shell_command, file_command, service_api):
    # Import raw task list
    resp = service_api.query(
        service = SCHEDULER,
        query = '''
            mutation {
                importTaskList(path: "/mission-app-1/testTask.json", name: "testTask", mode: "testMode") {
                    success,
                    errors
                }
            }
        '''
    )
    print(resp)
    assert(True == resp["importTaskList"]["success"])

@depends_on(step_schedule_app)
def step_verify_ran(shell_command, file_command, service_api):
    time.sleep(1)
    resp = service_api.query(
        service = APP,
        query = '''
        {
            appStatus {
                name
                pid
                endTime
            }
        }
        '''
    )
    print(resp)
    assert(1 == len(resp["appStatus"]))
    assert("test-mission-app-1" == resp["appStatus"][0]["name"])
    assert(resp["appStatus"][0]["endTime"] is not None)


def step_cleanup(shell_command, file_command, service_api):
    
    # Cleanup
    for i in range(1, 6):
        q = '''
            mutation {
                uninstall(name: "test-mission-app-%d") {
                    success
                }
            }
            ''' % i
        service_api.query(
            service = APP,
            query = q
        )

        shell_command(["run", "-c", "rm -rf /mission-app-{}".format(i)])

    service_api.query(
        service = SCHEDULER,
        query = '''
        mutation {
            safeMode{
                success
            }
        }
        '''
    )

    service_api.query(
        service = SCHEDULER,
        query = '''
        mutation {
            removeMode(name: "testMode") {
                success
            }
        }
        '''
    )
    

@test_steps(step_cleanup, step_prepare, step_register, step_create_mode, step_activate_mode, step_schedule_app, step_verify_ran)
#@test_steps(step_cleanup, step_prepare, step_register, step_cleanup)
def test_suite(test_step, shell_command, file_command, service_api):
    test_step(shell_command, file_command, service_api)

