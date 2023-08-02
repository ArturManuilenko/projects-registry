#!/bin/bash

echo ">>> $(basename ${BASH_SOURCE[0]})"

set -o errexit
set -o pipefail
set -o nounset



# INIT WORKING DIR
# ======================================================================================================
cd "$(dirname "${BASH_SOURCE[0]}")"
cd ../
CWD="$(pwd)"


# ENV
# ======================================================================================================

export PYTHONUNBUFFERED=1
export PYTHONPATH="${CWD}"


TEST_PY_FILES=`find . -type f -name "*__test.py" ! -path './.*'`
echo "$TEST_PY_FILES"

echo "RUN UNIT TESTS"
pytest --maxfail=1 -rf -l --cov=. --cov-report=term --cov-report=html:.var/test_coverage_html --cov-report=xml:.var/coverage.xml --junit-xml=.var/junit.xml ${TEST_PY_FILES} --ignore=${CWD}/src/vendor

echo "DONE"
