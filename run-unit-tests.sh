#!/bin/bash

# Defines directories to be added to PYTHONPATH
dirs=(
  lambda/create
  lambda/create/packages
  # Add more directories if necessary
)

# Combines directories with the appropriate delimiters
PYTHONPATH=$(IFS=:; echo "${dirs[*]}")

# Exports the PYTHONPATH variable
export PYTHONPATH

# Executes pytest
python -m pytest tests/unit/
