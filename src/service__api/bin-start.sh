#!/bin/bash

echo ">>> $(basename ${BASH_SOURCE[0]})"

set -o errexit
set -o pipefail
set -o nounset



# INIT WORKING DIR
# ======================================================================================================
cd "$(dirname "${BASH_SOURCE[0]}")"
cd ../../
CWD="$(pwd)"



# ARGS
# ======================================================================================================

APPLICATION_RELOAD="${APPLICATION_RELOAD:-0}"
APPLICATION_WORKERS="${APPLICATION_WORKERS:-*}"
APPLICATION_PORT="${APPLICATION_PORT:-8000}"


if [ "${APPLICATION_WORKERS}" == "*" ]; then
  APPLICATION_WORKERS=$(expr 1 + $(grep -c ^processor /proc/cpuinfo))
fi

echo "APPLICATION_PORT=${APPLICATION_PORT}"
echo "APPLICATION_WORKERS=${APPLICATION_WORKERS}"
echo "APPLICATION_RELOAD=${APPLICATION_RELOAD}"


# ENV
# ======================================================================================================

export PYTHONUNBUFFERED=1
export PYTHONPATH="${CWD}"
export FLASK_APP="${CWD}/src/service__api/main.py"
APP_MODULE="src.service__api.main"


# WAIT
# ======================================================================================================

#source /docker_app/src/service_db/bin-waiting.sh

# START
# ======================================================================================================
if [ "${APPLICATION_RELOAD}" == "0" ]; then
    echo "NORMAL START"
    echo ""
    gunicorn -w ${APPLICATION_WORKERS} --timeout 120 ${APP_MODULE}:app -b 0.0.0.0:${APPLICATION_PORT} --capture-output --access-logfile
else
    echo "RELOAD START"
    echo ""
    gunicorn -w ${APPLICATION_WORKERS} --timeout 120 ${APP_MODULE}:app -b 0.0.0.0:${APPLICATION_PORT} --capture-output --access-logfile - --reload
fi
