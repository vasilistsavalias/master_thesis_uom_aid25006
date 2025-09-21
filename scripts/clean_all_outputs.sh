#!/bin/bash
set -e

echo "===================================================================="
echo "Clean All Project Artifacts"
echo "===================================================================="
echo "This script will delete all generated outputs, including data,"
echo "models, and logs."
echo

read -p "Are you sure you want to continue? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Aborted."
    exit 1
fi

echo "Deleting log files..."
rm -rf logs

echo "Deleting pipeline stage outputs..."
# Find all directories starting with "0" and delete their "output" subdirectory
find 0* -type d -name 'output' -exec rm -rf {} +

echo
echo "===================================================================="
echo "Project cleaning complete."
echo "===================================================================="
echo
