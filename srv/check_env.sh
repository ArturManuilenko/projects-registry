#!/bin/bash

#echo ">>> $(basename ${BASH_SOURCE[0]})"

set -o errexit
set -o pipefail
set -o nounset



# INIT WORKING DIR
# ======================================================================================================
cd "$(dirname "${BASH_SOURCE[0]}")"
cd ../
CWD="$(pwd)"


# FUNC
# ======================================================================================================
RC='\e[31m'
GC='\e[32m'
YC='\e[33m'
NC='\e[39m'

check_pyenv(){
  E="$1";
  P=$(which $E);
  if [ -z "${P##*/.pyenv*}" ] ; then {
    SOME=""
    # do nothing
  } else {
    echo ""
    echo -e "${RC}ERROR${NC}: Path to ${YC}${E}${NC} bin must have '.pyenv' prefix in path. '${RC}${P}${NC}' was given";
    echo ""
    exit 1;
  } fi
}

check_pipenv(){
  E="$1";
  P=$(which $E);
  if [ -z "${P##*/virtualenvs/*}" ] ; then {
    SOME=""
    # do nothing
  } else {
    echo ""
    echo -e "${RC}ERROR${NC}: Path to ${YC}${E}${NC} bin must have '/virtualenvs/' prefix in path. '${RC}${P}${NC}' was given";
    echo ""
    exit 1;
  } fi
}

check_version() {
  E=$1
  P=$2
  V=$3

  if [ -z "${P##*$V*}" ] ; then {
    SOME=""
#    echo "$E $P $V"
    # do nothing
  } else {
    echo ""
    echo -e "${RC}ERROR${NC}: ${YC}${E} is incorrect${NC}. must be '$V'. '${RC}${P}${NC}' was given";
    echo ""
    exit 1;
  } fi
}


# RUN
# ======================================================================================================
check_pipenv "python"
check_pipenv "python3"
check_pyenv "docker-compose"
check_pyenv "pipenv"
check_pipenv "pip3"

PY_VERSION_DEST=$(cat ${CWD}/.python-version)

check_version "python3" "$(python3 --version)" "Python $PY_VERSION_DEST"
#check_version "python" "$(python --version)" "Python $PY_VERSION_DEST"
check_version "pipenv" "$(pipenv --version)" "pipenv, version 2021.5.29"
check_version "pip3" "$(pip3 --version)" "pip 21."
check_version "docker-compose" "$(docker-compose --version)" "docker-compose version 1.29."
#check_version "docker" "$(docker --version)" "Docker version 20.10."

echo -e ">>> ${GC}EVERYTHING IS OK${NC}"

