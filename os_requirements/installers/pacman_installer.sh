#!/bin/bash

function hello_world() {
    echo "HELLO WORLD"
}


function get_requirements_file_path() {
    work_dir=$1
    disto_name=$2
    echo "${work_dir}/pacman/requirements-${disto_name}.pacman"
}


function list_packages() {
    work_dir=$1
    disto_name=$2
    requirement_file_name=$(get_requirements_file_path "$work_dir" "$disto_name")

    grep -v "#" "${requirement_file_name}" | grep -v "^$";
}


function install_packages() {
    work_dir=$1
    disto_name=$2

    list_packages "$work_dir" "$disto_name" | xargs pacman -S --noconfirm
}
