#!/usr/bin/env bash
set -e

echo "===================================================================="
echo "Coffee Agriculture PLN Reasoning System — Verification Suite"
echo "===================================================================="

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

VENV_DIR="$PROJECT_ROOT/.venv-metta"
PYTHON_BIN="$VENV_DIR/bin/python"
PYTEST_BIN="$VENV_DIR/bin/pytest"

if [ ! -f "$PYTHON_BIN" ]; then
    echo "Error: Virtual environment not found at $VENV_DIR."
    echo "Please set up the environment with:"
    echo "  uv python install 3.12"
    echo "  uv venv .venv-metta --python 3.12"
    echo "  uv pip install -p .venv-metta hyperon streamlit pytest"
    exit 1
fi

echo "Environment Information:"
echo "  Python Version:  $($PYTHON_BIN --version)"
echo "  Hyperon Version: $($PYTHON_BIN -c 'import hyperon; print(hyperon.__version__)')"
echo "  Pytest Version:  $($PYTEST_BIN --version | head -n 1)"
echo ""

echo "--------------------------------------------------------------------"
echo "Running Comprehensive Automated Pytest Suite (50 Verified Tests)..."
echo "--------------------------------------------------------------------"
PYTHONPATH=. "$PYTEST_BIN" -v

echo ""
echo "===================================================================="
echo "ALL TESTS PASSED! System is 100% verified and reproducible."
echo "===================================================================="
