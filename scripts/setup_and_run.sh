#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- 1. Setup Virtual Environment ---
echo ">>> Setting up Python virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# --- 2. Activate Virtual Environment ---
echo ">>> Activating virtual environment..."
source .venv/bin/activate

# --- 3. Install Dependencies ---
echo ">>> Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# --- 4. Install Project Package ---
echo ">>> Installing project package in editable mode..."
pip install -e .

# --- 5. Run the Pipeline ---
echo ">>> Running the main pipeline..."
python main.py "$@"

echo ">>> Pipeline execution finished."
