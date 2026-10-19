#!/bin/bash
set -e

# Run the sync without allowing uv to perform a destructive directory rebuild
uv sync --all-extras
