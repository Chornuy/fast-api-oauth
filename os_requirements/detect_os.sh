#!/bin/bash


function detect_os_by_release() {
    echo >&2 -e "Detection OS \n"

    declare -A osInfo;
    osInfo[/etc/redhat-release]=yum
    osInfo[/etc/arch-release]=pacman
    osInfo[/etc/gentoo-release]=emerge
    osInfo[/etc/SuSE-release]=zypp
    osInfo[/etc/debian_version]=apt-get
    osInfo[/etc/alpine-release]=apk

    for f in "${!osInfo[@]}"
    do
        if [[ -f $f ]];then

            echo "${osInfo[$f]}"
            return 0
        fi
    done
    echo "FALLL"
    echo >&2 -e "Could not detect supporting OS for installing dependecies \n"
    exit 0
}
