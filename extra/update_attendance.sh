#!/bin/bash

# Set exit on error
set -e

# Change to the project directory
cd zoom-report

# Ensure poetry is in PATH
export PATH="$HOME/.local/bin:$PATH"

# Set up variables for retry logic
max_attempts=5
attempt_num=1

# Run the attendance script via poetry
until [[ $attempt_num -gt $max_attempts ]]; do
  if poetry run report -ar; then
    echo "Command succeeded on attempt $attempt_num."
    break
  else
    echo "Attempt $attempt_num failed. Trying again in 30 seconds..."
    sleep 30
    ((attempt_num++))
  fi
done

if [[ $attempt_num -gt $max_attempts ]]; then
  echo "All $max_attempts attempts failed. Exiting."
  exit 1
fi

exit 0
