#! /bin/bash

# Set to fall when script got an error
set -e
set -o pipefail

WORK_DIR="$(dirname "$0")"

DISTRO_NAME=$(lsb_release -sc | tr '[:upper:]' '[:lower:]')

# shellcheck source=detect_os.sh
source ./"$WORK_DIR"/detect_os.sh

PACKAGE_MANAGER=$(detect_os_by_release)

function list_packages(){
    grep -v "#" "${OS_REQUIREMENTS_FILENAME}" | grep -v "^$";
}


function get_installer_name() {
    work_dir="$1"
    packaga_manager="$2"
    echo "${work_dir}/installers/${packaga_manager}_installer.sh"
}


function get_python_requirements() {
    work_dir="$1"
    echo "${work_dir}/python_requirements/install.sh"
}


echo "OS NAME VARIABLE"
echo "$PACKAGE_MANAGER"

echo 'WORK DIR IS'
echo $WORK_DIR
echo "DISTRO NAME"
echo $DISTRO_NAME

installer_script=$(get_installer_name "$WORK_DIR" "$PACKAGE_MANAGER")
python_installer=$(get_python_requirements "$WORK_DIR")

# shellcheck source=detect_os.sh

source "$installer_script"
source "$python_installer"

if [ $EUID == 0 ]; then
  echo "This script mean to run as non root user"
  exit
fi

if [ $EUID != 0 ]; then
    sudo

    exit
fi

result=$(install_packages "$WORK_DIR" "$DISTRO_NAME")

echo $result
