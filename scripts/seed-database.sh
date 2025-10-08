#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

INITIAL_DIR=$(pwd)

PROJECT_ROOT=$(get_project_root)

setup_virtual_env "$PROJECT_ROOT" || {
    echo "Error: Failed to setup virtual environment"
    cd "$INITIAL_DIR"
    exit 1
}

install_python_deps "$PROJECT_ROOT" || {
    echo "Error: Failed to install Python dependencies"
    cd "$INITIAL_DIR"
    exit 1
}

navigate_to_server "$PROJECT_ROOT" "$INITIAL_DIR" || {
    exit 1
}

echo "Seeding database (idempotent)..."
run_python_script "utils/seed_database.py" || {
    echo "Error: Failed to run seed database script"
    cd "$INITIAL_DIR"
    exit 1
}

# Return to initial directory
cd "$INITIAL_DIR"
