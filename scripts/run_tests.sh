#!/bin/bash

echo "Starting Unit Tests"
python3 tests/unit_tests/polygon_helpers/polygon_helpers_test.py
python3 tests/unit_tests/polling_service/polling_service_test.py
python3 tests/unit_tests/email_service/email_service_test.py
echo "Finished Unit Tests"
echo "Starting Integration Tests"
python3 tests/integration_tests/polling_service/polling_service_integration_test.py
echo "Finished Integration Tests"