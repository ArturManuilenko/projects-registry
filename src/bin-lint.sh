#!/bin/bash

echo ">>> $(basename ${BASH_SOURCE[0]})"


set -o pipefail
set -o nounset
set -e


# INIT WORKING DIR
# ======================================================================================================
cd "$(dirname "${BASH_SOURCE[0]}")"
cd ../
CWD="$(pwd)"


# ENV
# ======================================================================================================

export PYTHONUNBUFFERED=1
export PYTHONPATH="${CWD}"


# check where and why script exit
# exec {BASH_XTRACEFD}> >(tail -n 1)
# PS4=':At line $LINENO; prior command exit status $?+'
# set -x

# INIT COLOR HIGHLIGHTING
# ===================================================

RED='\033[0;31m'
RED_BG='\e[41m'
BLACK='\e[1;30m'
CYAN='\e[36m'
BLUE='\033[0;34m'
GREEN='\033[0;32m'
NC='\033[0m'

process_counter=0
function start_section() {
    process_counter=$((process_counter+1))
    echo -e "${BLUE}[ STEP ${process_counter} : ${1} ]${NC}\n"
}
function end_section() {
    COUNT_OF_ERRORS=$1
    if (( ${COUNT_OF_ERRORS} > 0))
    then
        echo -e "\n${RED}[ FAILED : ${1} ERRORS FOUND ]\n"
        exit 1
    else
        echo -e "\n${GREEN}[ DONE without errors ]${NC}\n"
    fi
}


# SEARCH ALL PY FILES
# ==================================================

PY_FILES=`find ${CWD}/src -type f -name "*.py" ! -path './.*' -not -path "**/migrations/*" -not -path "**/test_requests/*" -not -path "*/vendor/*"`
echo "$PY_FILES"

# SHOW ENV VERSIONS
# ===================================================
# set +e
# echo "VERSIONS"
# echo python: "$(python --version)"
# echo python3: "$(python3 --version)"
# echo pipenv: "$(pipenv --version)"
# echo pip: "$(pip --version)"
# echo pip3: "$(pip --version)"
# echo mypy: "$(pip show mypy)"
# echo flake8: "$(pip show flake8)"
# echo pylint: "$(pip show pylint)"
# echo pycodestyle: "$(pip show pycodestyle)"
# set -e
# echo "END VERSIONS"

# RUN LINTING
# ===================================================

export PYTHONPATH=${CWD}


start_section "TYPE CHECKING : MYPY"
cd ${CWD}
set +e
python3.8 -m mypy ${PY_FILES} --show-traceback
MYPY_RESULT=$(mypy ${PY_FILES} --show-traceback)
set -e

SAVEIFS=$IFS
IFS=$'\n'
MYPY_RESULT_LINES=(${MYPY_RESULT})
IFS=$SAVEIFS
ERROR_LINES_COUNTER=0
for (( i=0; i<${#MYPY_RESULT_LINES[@]}; i++ ))
do
    _LINE=${MYPY_RESULT_LINES[${i}]}

    if (( ${#_LINE} > 1 ))
    then
        ERROR_LINES_COUNTER=${i}
    fi
done

end_section ${ERROR_LINES_COUNTER}


start_section "LINTING PEP 8"
cd ${CWD}
set +e
pycodestyle $PY_FILES --max-line-length=200
PYCODESTYLE_RESULT=$(pycodestyle $PY_FILES --max-line-length=200)
set -e

SAVEIFS=$IFS
IFS=$'\n'
PYCODESTYLE_RESULT_LINES=(${PYCODESTYLE_RESULT})
IFS=$SAVEIFS
ERROR_LINES_COUNTER=0
for (( i=0; i<${#PYCODESTYLE_RESULT_LINES[@]}; i++ ))
do
    _LINE=${PYCODESTYLE_RESULT_LINES[${i}]}

    if (( ${#_LINE} > 1 ))
    then
        ERROR_LINES_COUNTER=$((ERROR_LINES_COUNTER+1))
    fi
done

end_section ${ERROR_LINES_COUNTER}


start_section "LINTING FLAKE"
cd ${CWD}
set +e
flake8 $PY_FILES
ERRORS=$(flake8 $PY_FILES --count)
IFS=$'\n'; COUNT_OF_ERRORS=($ERRORS); unset IFS;
set -e
end_section "${COUNT_OF_ERRORS[-1]}"


start_section "LINTING PYLINT"
cd ${CWD}
set +e
python3.8 -m pylint --errors-only -j 4 **/*.py
set -e
end_section 0

printf "${GREEN}DONE${NC}\n"
