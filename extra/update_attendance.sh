#!/bin/bash

# Set exit on error
set -e

# Change to the project directory
cd zoom-report

# Ensure poetry is in PATH
export PATH="$HOME/.local/bin:$PATH"

# Run the attendance script via poetry
poetry run report -ar

exit 0
