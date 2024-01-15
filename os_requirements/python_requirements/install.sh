#!/bin/bash

function set_up_python_deps() {
    pipenv install --python python3.11

    pre-commit install
}
